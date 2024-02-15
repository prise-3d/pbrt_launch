""" Module pour extraire des informations d'un fichier EXR """

import OpenEXR
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"
import cv2

import numpy as np

print("start")

def exr_stats2(filename):
    print("start exr_stats2")
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH | cv2.EXR_TYPE_HALF)
    print(img.shape)
    # Loop over all pixels to display their value
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            pixel_value = img[i, j]
            if (i<2 and j<2):                
                print(f"Pixel at position ({i}, {j}): {pixel_value}")

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
        image = (flat_image.reshape(height, width)).ravel()
        print(image.shape)
        channel_means = np.mean(image)
        print("mean: ",channel_means)
        print(stats.describe(image))


if __name__ == "__main__":
    print("test for exr_stats")
    exr_stats2("test_data/bmw-m6.exr")
    exr_stats("test_data/bmw-m6-Integrators_Non_contributing_rays.exr")