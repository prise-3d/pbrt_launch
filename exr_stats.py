""" Module pour extraire des informations d'un fichier EXR """

import OpenEXR
import numpy as np
import argparse

print("start")

def exr_stats(filename):
    # Read the EXR image
    exr_file = OpenEXR.InputFile(filename)
    header = exr_file.header()

    # Get image size and channels
    width = header['dataWindow'].max.x + 1
    height = header['dataWindow'].max.y + 1
    channels = header['channels']

    print("image width ",width,"    height :",height,"    channels : ",channels)

    for k, v in channels.items():
        print(k, v)
        flat_image = np.frombuffer(exr_file.channel(k), dtype=np.float32) 
        #image = (flat_image.reshape(height, width)).ravel()
        #print(image.shape)
        channel_means = np.mean(flat_image)
        print("mean: ",channel_means)        

def main():
    parser = argparse.ArgumentParser(description='Script to produce statistics from a list of exr files')

    parser.add_argument('-b','--basedir', default='./output', help='Base directory where are exr files.')

    args = parser.parse_args()
    print(args.basedir)



if __name__ == "__main__":

    """

    print("test for exr_stats")
    exr_stats("test_data/bmw-m6.exr")
    print("--------------------")
    exr_stats("test_data/bmw-m6-Integrators_Non_contributing_rays.exr")

    """

    main()
    print("end")