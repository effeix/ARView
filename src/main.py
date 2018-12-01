import cv2
import numpy as np
import matplotlib.pyplot as plt


def origin_points(img):
    max_x = img.shape[1] - 1
    max_y = img.shape[0] - 1

    return np.array([
        (0, 0),
        (max_x, 0),
        (0, max_y),
        (max_x, max_y)
    ])

def dest_points(positions, ids):
    # Markers 0, 4, 30 and 34 are the in the corners of the ArUco board,
    # so we need the positions of these markers as destination points
    
    # Here, we get the median point of the corresponding marker.
    # We could also use the most external point

    dest = [
        np.median(positions[int(np.where(ids == 30)[0])][0], axis=0).astype(int).tolist(),
        np.median(positions[int(np.where(ids ==  0)[0])][0], axis=0).astype(int).tolist(),
        np.median(positions[int(np.where(ids == 34)[0])][0], axis=0).astype(int).tolist(),
        np.median(positions[int(np.where(ids ==  4)[0])][0], axis=0).astype(int).tolist()
    ]

    return np.array(dest)

def read_img(path):
    return cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)

CAMERA = 0
CAMERA_WAIT = 30
ARUCO = read_img("../images/board_aruco.png")
CAR = read_img("../images/car.jpg")

MARKERS_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
POS_ORIGIN, IDS_ORIGIN, _ = cv2.aruco.detectMarkers(ARUCO, MARKERS_DICT)

VERTEX_MARKERS = [[0], [4], [30], [34]] 

if __name__ == "__main__":
    cap = cv2.VideoCapture(CAMERA)
    ORIGIN = origin_points(CAR)

    while True:
        _, frame = cap.read()

        positions_dest, ids_dest, _ = cv2.aruco.detectMarkers(frame, MARKERS_DICT)
        
        if positions_dest:
            cv2.aruco.drawDetectedMarkers(frame, positions_dest)

            # If all corner markers can be seen
            if all(i in ids_dest for i in VERTEX_MARKERS):

                # Get coords for corner markers
                dest = dest_points(positions_dest, ids_dest)

                H, _ = cv2.findHomography(ORIGIN, dest)

                # Warp the image according to the computed homography
                # i.e. apply a transformation so the image matches the position
                # and translation of the ArUco board in the camera
                warped = cv2.warpPerspective(CAR, H, (frame.shape[1], frame.shape[0]))

                # Mask and merge the frame and the desired image
                # Frame and the warped image are "multiplied" and can be seen together
                warped[warped == 0] = frame[warped == 0]

                cv2.imshow("ARView", warped)
            else:
                # Show the frame if not all corner markers are showing
                cv2.imshow("ARView", frame)
        else:
            # Show the frame if there is no detection at all
            cv2.imshow("ARView", frame)

        key = cv2.waitKey(CAMERA_WAIT)

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
