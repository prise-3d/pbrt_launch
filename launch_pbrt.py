import os
import sys
import shutil
import subprocess
import json
import argparse


# output directory
# output_dir = "./out"
# os.makedirs(output_dir)

# path to pbrt v4 scenes
scenes_path = "/home/samuel/Documents/pbrt-v4-scenes"


# Assuming Integrator data is stored in a file named 'Integrator.json'
file_path_inte = "./json/Integrator.json"
with open(file_path_inte, 'r') as file:
    # Load JSON data from the file
    integrators = json.load(file)

# Assuming Sampler data is stored in a file named 'Sampler.json'
file_path_samp = "./json/Sampler.json"
with open(file_path_samp, 'r') as file:
    # Load JSON data from the file
    samplers = json.load(file)

# Assuming Scene data is stored in a file named 'Scene.json'
file_path_scene = "./json/Scene.json"
with open(file_path_scene, 'r') as file:
    # Load JSON data from the file
    scenes = json.load(file)

def create_directory(directory_path, force):
    """
    Create a directory at the specified path. If the directory already exists, prompt the user to confirm overwriting.

    Parameters:
    - directory_path (str): The path of the directory to be created or overwritten.
    - force (bool): If True, overwrite the directory without confirmation. If False, prompt the user for confirmation.

    Raises:
    - SystemExit: If the user chooses not to overwrite the existing directory, the program is terminated with exit code 1.
    """

    # Test if the directory exists
    if os.path.exists(directory_path):
        if force :
            choice = 'y'
        else :
            choice = input(f"The directory {directory_path} already exists. Do you want to overwrite it? (Y/N): ").lower()
        if choice == 'y':
            # Remove the existing directory and recreate it
            shutil.rmtree(directory_path)
            os.mkdir(directory_path)
            print(f"Directory {directory_path} recreated.")
        else:
            print("Program terminated.")
            sys.exit(1)
    else:
        # Create the directory if it doesn't exist
        os.mkdir(directory_path)
        print(f"Directory {directory_path} created.")    


# Répertoire temporaire pour stocker les fichiers modifiés
temp_dir = "temp_directory"
# if not os.path.exists(temp_dir):
#     os.makedirs(temp_dir)


# to remove an element of text
def remove_lines_starting_with(text, start_string):
    lines = text.splitlines()
    result_lines = []
    remove_next_lines = False

    for line in lines:
        if line.strip().startswith(start_string):
            # Set the flag to remove following lines
            remove_next_lines = True
        elif remove_next_lines and (line.startswith(" ") or line.startswith("\t")):
            # Skip lines beginning with space or tab
            continue
        else:
            # Add the line to the result if it's not to be removed
            result_lines.append(line)
            # Reset the flag if a new line is encountered
            remove_next_lines = False

    # Join the result lines into a new text
    result_text = '\n'.join(result_lines)
    return result_text



def remove_in_file(file, element):

    """
    Remove lines in the given text that start with the specified string, along with any following indented lines.

    Parameters:
    - text (str): The input text containing multiple lines.
    - start_string (str): The string indicating the lines to be removed.

    Returns:
    str: The modified text with lines starting with the specified string removed.
    """

    
    with open(file, 'r') as scene_file:
        scene_content = scene_file.read()

    modified_content = remove_lines_starting_with(scene_content, element)

    with open(file, 'w') as scene_file:
        scene_file.write(modified_content)


def add_in_file(file, before_string, element):
    """
    Add the specified element in the file before the line starting with the given string.

    Parameters:
    - file (str): The path to the file where the element is to be added.
    - before_string (str): The string indicating the line before which the element should be added.
    - element (str): The element to be added in the file.
    """

    with open(file, 'r') as file_content:
        content = file_content.read()

    lines = content.splitlines()
    modified_lines = []

    for line in lines:
        if line.strip().startswith(before_string):
            # Add the new element before the line that starts with before_string
            modified_lines.append(element)
        # Add the current line to the modified content
        modified_lines.append(line)

    modified_content = '\n'.join(modified_lines)

    with open(file, 'w') as file_content:
        file_content.write(modified_content)        

def run_pbrt(scenes_list, sampler_list, integrator_list, args) :
    """
    Run the PBRT renderer on a list of scenes with different samplers and integrators.

    Parameters:
    - scenes_list (list): A list of dictionaries containing information about scenes.
    - sampler_list (list): A list of dictionaries containing information about samplers.
    - integrator_list (list): A list of dictionaries containing information about integrators.
    - args (Namespace): Command-line arguments.
    """

    create_directory(args.output, args.force)

    for scene in scenes_list:
        scene_full_path = os.path.join(scenes_path, scene['path'])
        dirname = os.path.dirname(scene_full_path)
        filename = os.path.basename(scene_full_path)
        basename, old_ext = os.path.splitext(filename)
        os.makedirs(os.path.join(args.output,basename))
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        shutil.copytree(dirname, temp_dir)    

        for sampler in sampler_list:

            s_name = sampler['name']
            s_text = sampler['text']

            remove_in_file(os.path.join(temp_dir,filename), "Sampler")
            add_in_file(os.path.join(temp_dir,filename), "WorldBegin", s_text)

            # Display all key-value pairs
            for integrator in integrator_list:

                i_name = integrator['name']
                i_text = integrator['text']

                remove_in_file(os.path.join(temp_dir,filename), "Integrator")
                add_in_file(os.path.join(temp_dir,filename), "WorldBegin", i_text)
                
                outfile = os.path.join(args.output,basename,(basename+"_"+s_name+"_"+i_name+".exr"))

                cmd = "".join([args.pbrt," --spp ",str(args.spp)," ",
                            "--outfile ",outfile," ",
                            os.path.join(temp_dir,filename)])
                result = subprocess.run(cmd, shell=True)

                # Check the return code
                if result.returncode == 0:
                    print("Command executed successfully.")
                else:
                    print(f"Error: Command returned a non-zero exit code {result.returncode}.")
                    if result.returncode == 127 :
                        print("add pbrt to your path or use --pbrt option")

        # Clean    
        shutil.rmtree(temp_dir)

def main():
    """
    Parse the command line arguments and call run_pbrt
    """
    print("Launch pbrt")
    parser = argparse.ArgumentParser(description='Script to launch pbrt and produce images from a varety of Sampler and Integrator for a list of scenes')
     # Add a command line argument
    parser.add_argument('--spp', type=int, default=64, help='sample per pixel')
    parser.add_argument('-f', '--force', action='store_true', help='Force mode.')
    parser.add_argument('-o','--output', default='./output', help='Output directory path with default value "./output".')
    parser.add_argument('-p','--pbrt', default='pbrt', help='path and name of pbrt binary (default = "pbrt")')
    args = parser.parse_args()
    run_pbrt(scenes, samplers, integrators, args)


if __name__ == "__main__":
    main()   