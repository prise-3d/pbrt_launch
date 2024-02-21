""" Module pour extraire des informations d'un fichier EXR """

import csv
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

    list_values = []
    sampler = re.search(r'([^_]+)_[^_]+-Integrators', filename).group(1)
    integrator = re.search(r'[^_]+_([^_]+)-Integrators', filename).group(1)

    list.append(sampler)
    list.append(integrator) 

    for k, v in channels.items():
        print(k, v)
        flat_image = np.frombuffer(exr_file.channel(k), dtype=np.float32) 
        #image = (flat_image.reshape(height, width)).ravel()
        #print(image.shape)
        channel_means = np.mean(flat_image)
        list_values.append(channel_means)

    return list_values    

def main():
    parser = argparse.ArgumentParser(description='Script to produce statistics from a list of exr files')

    parser.add_argument('-b','--basedir', default='./output', help='Base directory where are exr files.')
    parser.add_argument('-e','--extension', default='.exr', help='end suffix of files to analyse (default .exr)')
    parser.add_argument('-o', '--output', default='output.csv', help='Output CSV file name (default: output.csv)')

    args = parser.parse_args()
    end = args.extension
    basedir = args.basedir
    import os

    # Scan all subdirectories and find the list of ".exr" files
    exr_files = []
    for root, dirs, files in os.walk(basedir):
        for file in files:
            if file.endswith(end):              
                exr_files.append(os.path.join(root, file))


    # Create a CSV file to store the statistics
    csv_filename = args.output
    for exr_file in exr_files:
        l = exr_stats(exr_file)
        csvfile = open(csv_filename, 'a', newline='')
        csv_writer = csv.writer(csvfile)
        row = [exr_file]
        for v in l:
            row.append(v)
        csv_writer.writerow(row)
        csvfile.close()


if __name__ == "__main__":

    """

    print("test for exr_stats")
    exr_stats("test_data/bmw-m6.exr")
    print("--------------------")
    exr_stats("test_data/bmw-m6-Integrators_Non_contributing_rays.exr")

    """

    main()
    print("end")