# pbrt_launch
python script to launch pbrt with different Samper/Integrator


Launch pbrt
usage: launch_pbrt.py [-h] [--spp SPP] [--format FORMAT] [-f] [-o OUTPUT] [-b BASEDIR] [-p PBRT]

Script to launch pbrt and produce images from a varety of Sampler and Integrator for a list of scenes

optional arguments:
  -h, --help            show this help message and exit
  --spp SPP             sample per pixel
  --format FORMAT       File extension for output file (default exr)
  -f, --force           Force mode.
  -o OUTPUT, --output OUTPUT
                        Output directory path with default value "./output".
  -b BASEDIR, --basedir BASEDIR
                        Base directory for pbrt scenes.
  -p PBRT, --pbrt PBRT  path and name of pbrt binary (default = "pbrt")

