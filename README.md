# ARView
Simple augmented reality project

## Explanation
The goal of this project is to project an image on an ArUco board. To do this we need to get the original image, calculate the homography needed to transform the image to the same pose as the board, and finally multiply the camera frame and the transformed image so it appears on the board.

First, we detect the ArUco markers, get the corner points of the board, get the corner points of the desired image, discover an homography that transforms the image to the same pose as the board and then warp the image using the detected markers.

The result is shown below:

![](./images/example.jpg)

## Usage
To execute, use:
```sh
$ python main.py <img_path>
```

where `img_path` is the path to the image to be applied to the board.

## Future work
- [ ] Project 3D objects
- [ ] Project in surface
