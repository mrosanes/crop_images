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
    def __init__(self, inputfile, inputtree, newhdf5):
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
        self.crop_top_rows = c_tr = int(raw_input(
                      "Number of top rows to be cropped: "))
        self.crop_bottom_rows = c_br = int(raw_input(
                      "Number of bottom rows to be cropped: "))
        self.crop_left_columns = c_lc = int(raw_input(
                      "Number of left columns to be cropped: "))
        self.crop_right_columns = c_rc = int(raw_input(
                      "Number of right columns to be cropped: "))

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





