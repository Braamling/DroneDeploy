import numpy as np
import cv2

class PerspectiveTracker():

    def __init__(self, config):
        self.config = config
        self.pattern = cv2.imread(config.pattern_path,0)
        self.photo = cv2.imread(config.image_path,0)

        # Setup camera calibration
        self.calibrateIphone6()

      
    """ Calibrates the camera to the estimation of an iphone 6 
        camera. The calibration parameters are based on the following post:
        https://stackoverflow.com/questions/34963337/iphone-6-camera-calibration-for-opencv
    """
    def calibrateIphone6(self):
        fx = 1229
        cx = self.photo.shape[1]/2
        fy = 1153
        cy = self.photo.shape[0]/2 

        self.cm_matrix = np.float32([[fx, 0, cx], [0, fy, cy], [0, 0, 1]]).reshape(-1,3)

    """ Detects sift keypoints in both the photo and pattern and finds 
        All matching keypoints
    """
    def detectKeyPoints(self):
        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(self.photo,None)
        kp2, des2 = sift.detectAndCompute(self.pattern,None)

        # Match the found keypoints
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2, k=2)

        # Keep all keypoints pairs that are within the provided threshold.
        src_points = []
        dst_points = []
        for m,n in matches:
            if m.distance < self.config.sift_threshold * n.distance:
                src_points.append(kp1[m.queryIdx].pt)
                dst_points.append(kp2[m.trainIdx].pt + (0,))

        self.src_points = np.asarray(src_points)

        # 'translate' the pattern image to a 3d plane by adding a z axis
        self.dst_points = np.asarray(dst_points)[:, :, np.newaxis] 

    """
    Use the found matching keypoints to construct the camera perspective
    """
    def getCameraPerspective(self):
        # Get the rotation and translation vectors.
        # The implementation was influenced by the following stackoverflow page:
        # http://answers.opencv.org/question/161369/retrieve-yaw-pitch-roll-from-rvec/
        _, rvec, tvec, _ = cv2.solvePnPRansac(self.dst_points, self.src_points, self.cm_matrix, distCoeffs=None)

        rmatrix = cv2.Rodrigues(rvec)[0]

        cam_pos = -np.matrix(rmatrix).T * np.matrix(tvec)

        P = np.hstack((rmatrix,tvec))

        euler_angles_radians = -cv2.decomposeProjectionMatrix(P)[6]

        return euler_angles_radians, cam_pos
