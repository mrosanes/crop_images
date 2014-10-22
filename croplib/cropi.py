#!/usr/bin/python

# The following copyright statement and license apply to this code.
# Copyright (c) 2014 Marc Rosanes Siscart
#Permission is hereby granted, free of charge, to any person obtaining
#a copy of this software and associated documentation files (the
#"Software"), to deal in the Software without restriction, including
#without limitation the rights to use, copy, modify, merge, publish,
#distribute, sublicense, and/or sell copies of the Software, and to
#permit persons to whom the Software is furnished to do so, subject to
#the following conditions:
#The above copyright notice and this permission notice shall be included
#in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import numpy as np
import nxs
import os

class CropClass:

    ### Constructor of CropClass objects ###
    def __init__(self, inputfile, inputtree, crop, newhdf5):
        self.new = 0
        if (newhdf5 == 1):
            self.new = 1

        self.input_nexusfile = nxs.load(inputfile, mode='rw')

        #self.input_nexusfile = nxs.open(inputfile, 'rw') 
        self.ifilepathname = inputfile
        self.ifilepath = os.path.dirname(inputfile)
        self.ifilename = inputfile.split('/')[-1]
        self.itree = inputtree
        self.itreepath = 'None'
        if '/' in self.itree:
            self.itreepath = inputtree.rsplit('/', 1)[0]
            self.itreename = inputtree.rsplit('/', 1)[1]
        else:
            self.itreename = self.itree

        if (self.new == 1):
            self.outputfilehdf5 = inputfile.split('.hdf')[0]+'_crop'+'.hdf5'
            self.outcrop = nxs.NXentry(name= self.itreepath)
            self.outcrop.save(self.outputfilehdf5, 'w5')

        if not self.ifilepath:
            self.ifilepath = '.'
        self.crop = crop          

        # Stack dimensions
        self.nFrames = 0                
        self.numrows = 0
        self.numcols = 0
        self.dim_images = (0, 0, 1)

        # Image dimensions after cropping              
        self.numrows_ac = 0
        self.numcols_ac = 0

        self.crop_top_rows = 0
        self.crop_bottom_rows = 0
        self.crop_left_columns = 0
        self.crop_right_columns = 0
        return

    
    def cropFunc(self):

        print("cropping...")
        self.crop_top_rows = c_tr = 25 #raw_input(
                                       #"Number of top rows to be cropped: ")
        self.crop_bottom_rows = c_br = 25 #raw_input(
                                      # "Number of bottom rows to be cropped: ")
        self.crop_left_columns = c_lc = 25 #raw_input(
                                     #"Number of left columns to be cropped: ")
        self.crop_right_columns = c_rc = 25 #raw_input(
                                    #"Number of right columns to be cropped: ")

        cropentry = self.itreename + '_crop2'

        img_grp = self.input_nexusfile[self.itreepath]
        self.nFrames = img_grp[self.itreename].shape[0]
        self.numrows = img_grp[self.itreename].shape[1]
        self.numcols = img_grp[self.itreename].shape[2]
               
        self.numrows_ac = self.numrows - c_tr - c_br
        self.numcols_ac = self.numcols - c_lc - c_rc
        numimg = 0  

        ro_to = self.numrows - c_br 
        co_to = self.numcols - c_rc

        if (self.new == 0):
            img_grp[cropentry] = nxs.NXfield(
                      dtype='float32' , 
                      shape=[nxs.UNLIMITED, self.numrows_ac, self.numcols_ac])

            img_grp[cropentry].attrs['Number of Frames'] = self.nFrames
            img_grp[cropentry].attrs['Pixel Rows'] = self.numrows_ac
            img_grp[cropentry].attrs['Pixel Columns'] = self.numcols_ac
            img_grp[cropentry].write()

            for numimg in range(self.nFrames):
                image_retrieved = img_grp[self.itreename][
                                                 numimg, c_tr:ro_to, c_lc:co_to]
                img_grp[cropentry].put(image_retrieved, [numimg,0,0])
                print("image " + str(numimg) + " cropped")

            img_grp[cropentry].write()

        elif (self.new == 1):
            self.outcrop[cropentry] = nxs.NXfield(
                      dtype='float32' , 
                      shape=[nxs.UNLIMITED, self.numrows_ac, self.numcols_ac])

            self.outcrop[cropentry].attrs['Number of Frames'] = self.nFrames
            self.outcrop[cropentry].attrs['Pixel Rows'] = self.numrows_ac
            self.outcrop[cropentry].attrs['Pixel Columns'] = self.numcols_ac
            self.outcrop[cropentry].write()

            for numimg in range(self.nFrames):
                image_retrieved = img_grp[self.itreename][
                                                 numimg, c_tr:ro_to, c_lc:co_to]
                self.outcrop[cropentry].put(image_retrieved, [numimg,0,0])
                print("image " + str(numimg) + " cropped")
            img_grp[cropentry].write()













        """    
        print("###hih###")
        print image_retrieved[0][0][0]
        print(image_retrieved.shape)
        print("###hih###")

        print("#########")
        print(img_grp.TomoNormalized.attrs)
        print(img_grp.TomoNormalized.shape)
        print("#########")
        #print(self.input_nexusfile.TomoNormalized[cropentry])
        print(self.ifilepath)
        print(self.ifilepathname)
        print(self.ifilename)
        print(self.nFrames)
        print(self.input_nexusfile.__class__)
        """

















        #img_grp[cropentry].save()

        #print(image_retrieved)






        #img_grp[cropentry]
        #img_grp[cropentry] = image_retrieved
        #nxsfied.put(image, slab_offset, refresh=False)
        #img_grp[cropentry].write()




        """
        self.fastalign[self.data_nxs] = nxs.NXfield(
                        name=self.data_nxs, dtype='float32' , 
                        shape=[nxs.UNLIMITED, self.numrows, self.numcols])
        self.fastalign[self.data_nxs].attrs[
                                         'Number of Frames'] = self.nFrames
        self.fastalign[self.data_nxs].attrs[
                                                'Pixel Rows'] = self.numrows    
        self.fastalign[self.data_nxs].attrs[
                                             'Pixel Columns'] = self.numcols
        self.fastalign[self.data_nxs].write()    

        """







        #self.input_nexusfile.opengroup('TomoNormalized')
        #self.input_nexusfile.opendata(self.itreename)
        #slab_offset = [1, 0, 0]
        #nxsfied.put(image_retrieved, slab_offset, refresh=True)

        #print(self.input_nexusfile.tree)
        #print(self.input_nexusfile.TomoNormalized.TomoNormalized[0, 0 , 0])




















        """self.infoshape = self.input_nexusfile.getinfo()
        self.dim_images = (self.infoshape[0][0], self.infoshape[0][1], 
                               self.infoshape[0][2])
        self.nFrames = self.infoshape[0][0]
        self.numrows = self.infoshape[0][1]
        self.numcols = self.infoshape[0][2]"""










        """self.fastalign[self.data_nxs].attrs[
                                         'Number of Frames'] = self.nFrames
        self.fastalign[self.data_nxs].attrs[
                                                'Pixel Rows'] = self.numrows    
        self.fastalign[self.data_nxs].attrs[
                                             'Pixel Columns'] = self.numcols
        self.fastalign[self.data_nxs].write() """   




        """self.infoshape = self.input_nexusfile.getinfo()
        self.dim_images = (self.infoshape[0][0], self.infoshape[0][1], 
                               self.infoshape[0][2])
        self.nFrames = self.infoshape[0][0]
        self.numrows = self.infoshape[0][1]
        self.numcols = self.infoshape[0][2]"""




























































    """    

    ### How much to crop ###
    def lookForCrop(self, proj2_moved, cent_pix_rows, cent_pix_cols):
        crop_top_rows = 0
        crop_bottom_rows = 0
        crop_left_columns = 0
        crop_right_columns = 0
        ctr = crop_top_rows
        cbr = crop_bottom_rows
        clc = crop_left_columns
        crc = crop_right_columns

        rowtopsum = 0
        while rowtopsum == 0:
            rowtopsum = 0
            for col in range(cent_pix_cols-5, cent_pix_cols+5):
                rowtopsum = rowtopsum + proj2_moved[ctr][col]                        
            if(rowtopsum == 0):
                ctr = ctr + 1 

        rowbottomsum = 0
        while rowbottomsum == 0:
            rowbottomsum = 0
            for col in range(cent_pix_cols-5, cent_pix_cols+5):
                lastrow = proj2_moved.shape[0]-1
                rowbottomsum = rowbottomsum + proj2_moved[lastrow-cbr][col]                        
            if(rowbottomsum == 0):
                cbr = cbr + 1 

        colleftsum = 0
        while colleftsum == 0:
            colleftsum = 0
            for row in range(cent_pix_rows-5, cent_pix_rows+5):
                colleftsum = colleftsum + proj2_moved[row][clc]                        
            if(colleftsum == 0):
                clc = clc + 1   

        colrightsum = 0
        while colrightsum == 0:
            colrightsum = 0
            for row in range(cent_pix_rows-5, cent_pix_rows+5):
                lastcol = proj2_moved.shape[1]-1
                colrightsum = colrightsum + proj2_moved[row][lastcol-crc]                        
            if(colrightsum == 0):
                crc = crc + 1

        if (ctr > self.crop_top_rows):
            self.crop_top_rows = ctr                
        if (cbr > self.crop_bottom_rows):
            self.crop_bottom_rows = cbr
        if (clc > self.crop_left_columns):
            self.crop_left_columns = clc
        if (crc > self.crop_right_columns):
            self.crop_right_columns = crc 


    ### Align all projections ###
    def alignTomo(self):
        if self.spec == 0:
            self.input_nexusfile.opengroup('TomoNormalized')
        elif self.spec == 1:
            self.input_nexusfile.opengroup('SpecNormalized')

        ###################################    
        ## Retrieving data from angles   ##
        ###################################
        try: 
            self.input_nexusfile.opendata('rotation_angle')
            self.angles = self.input_nexusfile.getdata()
            self.input_nexusfile.closedata()
            
            self.fastalign['rotation_angle'] = self.angles
            self.fastalign['rotation_angle'].write()  
        except:
            print("\nAngles could NOT be extracted.\n")
            try:
                self.input_nexusfile.closedata()
            except:
                pass               


        ########################################   
        ## Retrieving data from images shape  ##
        ########################################
        if self.spec == 0:
            self.input_nexusfile.opendata('TomoNormalized')
        elif self.spec == 1:
            self.input_nexusfile.opendata('spectroscopy_normalized')

        self.infoshape = self.input_nexusfile.getinfo()
        self.dim_images = (self.infoshape[0][0], self.infoshape[0][1], 
                               self.infoshape[0][2])
        self.nFrames = self.infoshape[0][0]
        self.numrows = self.infoshape[0][1]
        self.numcols = self.infoshape[0][2]
        print("Dimensions: {0}".format(self.dim_images))
        self.input_nexusfile.closedata()
      
        self.fastalign[self.data_nxs] = nxs.NXfield(
                        name=self.data_nxs, dtype='float32' , 
                        shape=[nxs.UNLIMITED, self.numrows, self.numcols])
        self.fastalign[self.data_nxs].attrs[
                                         'Number of Frames'] = self.nFrames
        self.fastalign[self.data_nxs].attrs[
                                                'Pixel Rows'] = self.numrows    
        self.fastalign[self.data_nxs].attrs[
                                             'Pixel Columns'] = self.numcols
        self.fastalign[self.data_nxs].write()    
            

        #################################################   
        ## Get align and store aligned images in HDF5  ##
        #################################################
        if self.spec == 0:
            self.input_nexusfile.opendata('TomoNormalized')
            central_img_num = int(self.nFrames)/2
        elif self.spec == 1:
            self.input_nexusfile.opendata('spectroscopy_normalized')
            central_img_num = 0
            
        image_proj1 = self.getSingleImage(central_img_num)

        # proj1 is the image from which we extract the template
        proj1 = image_proj1[0, :, :]
        
        #cv2.imshow('proj1',proj1)
        #cv2.waitKey(0)
        slab_offset = [central_img_num, 0, 0]
        nxsfied = self.fastalign[self.data_nxs]
        self.writeImageInHdf5(image_proj1, nxsfied, slab_offset)
        print('Image %d stored\n' % central_img_num)

        # method = eval('cv2.TM_CCOEFF_NORMED')
        method = eval('cv2.TM_CCORR_NORMED')        

        central_pixel_rows = int(self.numrows/2)
        central_pixel_cols = int(self.numcols/2)
        width_tem = 300 
        height_tem = 500
  
        row_tem_from = central_pixel_rows - height_tem/2        
        row_tem_to = central_pixel_rows + height_tem/2
        col_tem_from = central_pixel_cols - width_tem/2
        col_tem_to = central_pixel_cols + width_tem/2

        #In openCV first we indicate the columns and then the rows.
        top_left_base = (col_tem_from, row_tem_from)

          self.input_nexusfile.closedata()      
        self.input_nexusfile.closegroup()     
        self.input_nexusfile.close()

        if(self.crop == 1):
            self.cropProjections()


    def cropProjections(self):

        #bc: before crop
        #ac: after crop
        nexusfile_aligned_bc = nxs.open(self.outputfilehdf5, 'r')
        nexusfile_aligned_bc.opengroup('FastAligned')

        fastalign_ac = nxs.NXentry(name= "FastAligned")
        fastalign_ac.save(self.outputfilehdf5_ac, 'w5')

        try: 
            nexusfile_aligned_bc.opendata('rotation_angle')
            self.angles = nexusfile_aligned_bc.getdata()
            nexusfile_aligned_bc.closedata()
            
            fastalign_ac['rotation_angle'] = self.angles
            fastalign_ac['rotation_angle'].write()  
        except:
            print("\nAngles could NOT be extracted.\n")
            try:
                nexusfile_aligned_bc.closedata()
            except:
                pass 

        numrows_ac = self.numrows - self.crop_top_rows - self.crop_bottom_rows
        numcols_ac = (self.numcols - self.crop_left_columns 
                                                    - self.crop_right_columns)

        fastalign_ac[self.data_nxs] = nxs.NXfield(
                        name=self.data_nxs, dtype='float32' , 
                        shape=[nxs.UNLIMITED, numrows_ac, numcols_ac])
        fastalign_ac[self.data_nxs].attrs[
                                         'Number of Frames'] = self.nFrames
        fastalign_ac[self.data_nxs].attrs[
                                                'Pixel Rows'] = self.numrows    
        fastalign_ac[self.data_nxs].attrs[
                                             'Pixel Columns'] = self.numcols
        fastalign_ac[self.data_nxs].write()

        nexusfile_aligned_bc.opendata(self.data_nxs)

        tr = self.crop_top_rows
        br = self.numrows-self.crop_bottom_rows
        lc = self.crop_left_columns
        rc = self.numcols-self.crop_right_columns
        nxsfied = fastalign_ac[self.data_nxs]

        print("\n")
        print("Cropping projections...")
        for numimg in range(0, self.nFrames):
            proj_not_cropped = nexusfile_aligned_bc.getslab(
                         [numimg, 0, 0], [1, self.numrows, self.numcols])
            
            pnc = proj_not_cropped
            proj = pnc[:, tr:br, lc:rc]
            
            slab_offset = [numimg, 0, 0]
            self.writeImageInHdf5(proj, nxsfied, slab_offset)
        print("Projections have been cropped")
        print("Cropped " + str(self.crop_top_rows) + " rows at top")
        print("Cropped " + str(self.crop_bottom_rows) + " rows at bottom")
        print("Cropped " + str(self.crop_left_columns) + " columns at left")
        print("Cropped " + str(self.crop_right_columns) + " columns at right")

        nexusfile_aligned_bc.closedata()      
        nexusfile_aligned_bc.closegroup()     
        nexusfile_aligned_bc.close()

        """



