import os
import shutil
import subprocess
import json
import argparse


# output directory
# output_dir = "./out"
# os.makedirs(output_dir)

# path to pbrt v4 
pbrt_exec = "/home/samuel/Documents/pbrt-v4/build/pbrt"

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

def create_directory(directory_path):
    # Test if the directory exists
    if os.path.exists(directory_path):
        choice = input("The directory already exists. Do you want to overwrite it? (Y/N): ").lower()
        if choice == 'y':
            # Remove the existing directory and recreate it
            os.rmdir(directory_path)
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
    
    with open(file, 'r') as scene_file:
        scene_content = scene_file.read()

    modified_content = remove_lines_starting_with(scene_content, element)

    with open(file, 'w') as scene_file:
        scene_file.write(modified_content)


def add_in_file(file, before_string, element):
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

    create_directory(args.output)

    for scene in scenes_list:
        scene_full_path = os.path.join(scenes_path, scene['path'])
        dirname = os.path.dirname(scene_full_path)
        filename = os.path.basename(scene_full_path)
        basename, old_ext = os.path.splitext(filename)
        shutil.copytree(dirname, temp_dir)
        os.makedirs(os.path.join(output_dir,basename))


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
                
                outfile = os.path.join(output_dir,basename,(basename+"_"+s_name+"_"+i_name+".exr"))

                cmd = "".join([pbrt_exec," --spp ",str(args.spp)," ",
                            "--outfile ",outfile," ",
                            os.path.join(temp_dir,filename)])
                subprocess.run(cmd, shell=True)

        # Clean    
        shutil.rmtree(temp_dir)

def main():
    print("Launch pbrt")
    parser = argparse.ArgumentParser(description='Script to launch pbrt and produce images from a varety of Sampler and Integrator for a list of scenes')
     # Add a command line argument
    parser.add_argument('--spp', type=int, default=64, help='sample per pixel')
    parser.add_argument('-f', '--force', action='store_true', help='Force mode.')
    parser.add_argument('-o','--output', default='./output', help='Output directory path with default value "./output".')
    args = parser.parse_args()
    run_pbrt(scenes, samplers, integrators, args)


if __name__ == "__main__":
    main()   