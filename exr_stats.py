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
    basedir = args.basedir
    import os

    # Scan all subdirectories and find the list of ".exr" files
    exr_files = []
    for root, dirs, files in os.walk(basedir):
        for file in files:
            if file.endswith(".exr"):
                exr_files.append(os.path.join(root, file))

    # Print the full path of all the ".exr" files
    for exr_file in exr_files:
        print(exr_file)



if __name__ == "__main__":

    """

    print("test for exr_stats")
    exr_stats("test_data/bmw-m6.exr")
    print("--------------------")
    exr_stats("test_data/bmw-m6-Integrators_Non_contributing_rays.exr")

    """

    main()
    print("end")