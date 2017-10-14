## Coding assignment for DroneDeploy
##### *Author: Bram van den Akker*

This repository contains the implementation for the DroneDeploy coding challenge. The assignment is to get the camera perspective from a picture of a sheet of paper containing a pattern and visualize the position and orientation. The implementation consists of a perspective tracker and perspective renderer. The perspective tracker uses `OpenCV` to collect sift keypoints and use `SolvePNP` to estimate the camera perspective. The perspective renderer uses `OpenGL` to reconstruct the scene in 3D using the provided image pattern. 

The code has been written in `Python 3.6.0`, please use a python3 when testing the implementation (both the pip and python were aliases of python3 in the examples) . All requirements can be installed using pip in the following fashion.

```
$ pip install -r requirements
```

The script has to be run with a pattern image and iphone image as arguments. 

```
usage: main.py [-h] pattern_path image_path

This script will use OpenCV and OpenGL in order to reconstruct the camera
orientation based on a pattern image and iphone6 picture. The code has been
submitted as part of the DroneDeploy code interview

positional arguments:
  pattern_path  Path to pattern image
  image_path    Path to image with pattern to be used for camera orientation
                reconstruction.

optional arguments:
  -h, --help    show this help message and exit
```

An example with valid arguments would be the following.
```
$ python main.py images/pattern.png images/IMG_6725
```
