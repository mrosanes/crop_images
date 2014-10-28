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


from croplib import cropi
import argparse

def main():
    parser = argparse.ArgumentParser(
                              description="Align the tomography projections \n")

    parser.add_argument('inputfile', type=str, default=None,
               help='Enter hdf5 file containing the images to be cropped')
    parser.add_argument('-t' ,'--inputtree', 
               type=str, default='TomoNormalized/TomoNormalized',
               help='Enter hdf5 tree containing the images to be cropped')
    parser.add_argument('-n', '--newhdf5', type=int, default=0, 
               help='Store cropped images in new hdf5')
                                 
    args = parser.parse_args()
    
    print("\nCrop images\n")
    crop_obj = cropi.CropClass(args.inputfile, 
                    args.inputtree, args.newhdf5)
    crop_obj.cropFunc()
    print("\nImages cropped\n\n")

if __name__ == "__main__":
    main()


