#!/usr/bin/python

"""
(C) Copyright 2014 Marc Rosanes
The program is distributed under the terms of the 
GNU General Public License (or the Lesser GPL).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np
import h5py
import os

class CropClass:

    ### Constructor of CropClass objects ###
    def __init__(self, inputfile, inputtree, storetree, newhdf5):

        self.inputh5 = h5py.File(inputfile, mode='r+')

        self.new = None
        if (newhdf5 != None):
            self.new = newhdf5

            if (self.new == "default"):
                self.outputfilehdf5 = inputfile.split('.hdf')[0]+'_crop'+'.hdf5'
            else:
                self.outputfilehdf5 = newhdf5
 
        self.ifilepathname = inputfile
        self.ifilepath = os.path.dirname(inputfile)
        self.ifilename = inputfile.split('/')[-1]
        self.itree = inputtree
        self.itreepath = 'None'
        if '/' in self.itree:
            self.itreepath = inputtree.rsplit('/', 1)[0]
            self.itreename = inputtree.rsplit('/', 1)[-1]
        else:
            self.itreename = self.itree

        self.storetree = storetree
        if self.storetree != None:
            if '/' in self.storetree:
                self.storetreepath = storetree.rsplit('/', 1)[0]
                self.storetreename = storetree.rsplit('/', 1)[-1]
            else:
                self.storetreename = self.storetree

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
        
        self.crop_top_rows = c_tr = 10 #int(raw_input(
                      #"Number of top rows to be cropped: "))
        self.crop_bottom_rows = c_br = 10 #int(raw_input(
                      #"Number of bottom rows to be cropped: "))
        self.crop_left_columns = c_lc = 200 #int(raw_input(
                      #"Number of left columns to be cropped: "))
        self.crop_right_columns = c_rc = 200 #int(raw_input(
                      #"Number of right columns to be cropped: "))

        cropentry = self.itreename + '_crop'
        #if self.storetree != None:
        #    cropentry = self.storetreename 
        try:
            ih5 = self.inputh5
            grps = self.itreepath.split('/')
            img_grp = ih5.get(grps[0])
            for i in range(1, len(grps)):
                img_grp = img_grp.get(grps[i])
            self.nFrames = img_grp[self.itreename].shape[0]
            self.numrows = img_grp[self.itreename].shape[1]
            self.numcols = img_grp[self.itreename].shape[2]
        except:
            print("Tree was not encountered in hdf5 file.")
            print("Please, specify a valid tree.\n")
            return
               
        self.numrows_ac = self.numrows - c_tr - c_br
        self.numcols_ac = self.numcols - c_lc - c_rc
        numimg = 0  

        ro_to = self.numrows - c_br 
        co_to = self.numcols - c_rc

        if (self.new == None):
            try:
                dsetcrop = img_grp.create_dataset(cropentry,
                            (self.nFrames, self.numrows_ac, self.numcols_ac), 
                            maxshape=(None, self.numrows_ac, self.numcols_ac), 
                            dtype='float32')
                dsetcrop.attrs['Number of Frames'] = self.nFrames
                dsetcrop.attrs['Pixel Rows'] = self.numrows_ac
                dsetcrop.attrs['Pixel Columns'] = self.numcols_ac
            except:
                print("\nError: The dataset %s probably exists already:" 
                      % cropentry)
                print("Delete it before continuing.\n")
                return

            for numimg in range(self.nFrames):
                image_retrieved = img_grp[self.itreename][
                                    numimg, c_tr:ro_to, c_lc:co_to]
                dsetcrop[numimg,:,:] = image_retrieved     
                print("image " + str(numimg) + " cropped")
  
        elif (self.new != None):
            f = h5py.File(self.outputfilehdf5, "w")
            groups = self.storetreepath.split('/')
            self.grpcrop = f.create_group(groups[0])
            for i in range(1, len(groups)):
                self.grpcrop = self.grpcrop.create_group(groups[i])
                
            dsetcrop = self.grpcrop.create_dataset(self.storetreename, 
                        (self.nFrames, self.numrows_ac, self.numcols_ac), 
                        maxshape=(None, self.numrows_ac, self.numcols_ac), 
                        dtype='float32')
            dsetcrop.attrs['Number of Frames'] = self.nFrames
            dsetcrop.attrs['Pixel Rows'] = self.numrows_ac
            dsetcrop.attrs['Pixel Columns'] = self.numcols_ac

            for numimg in range(self.nFrames):
                image_retrieved = img_grp[self.itreename][
                                    numimg, c_tr:ro_to, c_lc:co_to]
                dsetcrop[numimg,:,:] = image_retrieved     
                print("image " + str(numimg) + " cropped")

        print("\nImages cropped\n\n")

