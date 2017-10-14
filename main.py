from PerspectiveTracker import PerspectiveTracker
from PerspectiveRenderer import PerspectiveRenderer
import argparse

class Config():
    # The threshold used to match SIFT keypoints
    sift_threshold = 0.50

    # I had some problems with the translations in openGL
    # the translation was to far, which rendered to objects black
    # This was solved by scaling both translation and objects.
    scale = 15

    # Display size of the PyGame window.
    display_size = (800, 600)

    # The two input images
    pattern_path = 'images/pattern.png'
    image_path = 'images/IMG_6723.JPG'

    pattern_path_desc = "Path to pattern image"
    image_path_desc = """Path to image with 
    pattern to be used for camera orientation reconstruction.
    """

    argument_desc = """
    This script will use OpenCV and OpenGL in order to reconstruct the
    camera orientation based on a pattern image and iphone6 picture.

    The code has been submitted as part of the DroneDeploy code interview
    """


def main():
    config = Config()
    
    # Setup the argument parser
    parser = argparse.ArgumentParser(description=config.argument_desc)
    parser.add_argument('pattern_path', help=config.pattern_path_desc)
    parser.add_argument('image_path', help=config.image_path_desc)
        
    # Parse and apply the arguments.
    args = parser.parse_args()
    config.pattern_path = args.pattern_path
    config.image_path = args.image_path

    # Initiate all the requirements for the Perspective transform
    tracker = PerspectiveTracker(config)
    
    # # # # Retrieve the camera orientation
    tracker.detectKeyPoints()
    rvec, tvec = tracker.getCameraPerspective()

    # Render the found camera perspective 
    renderer = PerspectiveRenderer(config)
    renderer.positionCamera(rvec, tvec)
    renderer.render()


if __name__ == '__main__':
    main()