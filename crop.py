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


from croplib import cropi
import argparse

def main():
    parser = argparse.ArgumentParser(
                              description="Align the tomography projections \n")

    parser.add_argument('inputfile', type=str, default=None,
               help='Enter hdf5 file containing the images to be cropped')
    parser.add_argument('-t' ,'--inputtree', 
               type=str, default='TomoNormalized/TomoNormalized',
               help='Enter hdf5 tree containing the images to be cropped.\n' +
                    'Default: TomoNormalized/TomoNormalized')
    parser.add_argument('-s' ,'--storetree', 
               type=str, default='DataFolder/DataSet',
               help='Enter hdf5 tree where the cropped images will be stored.\n' +
                    'Default: DataFolder/DataSet')
    parser.add_argument('-n', '--newhdf5', type=int, default=0, 
               help='Store cropped images in new hdf5 (default=0)')
                                 
    args = parser.parse_args()
    
    print("\nCrop images\n")
    crop_obj = cropi.CropClass(args.inputfile, 
                    args.inputtree, args.storetree, args.newhdf5)
    crop_obj.cropFunc()

if __name__ == "__main__":
    main()


