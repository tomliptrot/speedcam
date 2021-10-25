import math

import cv2
import pandas as pd
import typer

from speedcam.frame import Frame


class Video:
    def __init__(self, frames: "list[Frame]", fps=30):
        self.frames = frames
        self.fps = fps

    @classmethod
    def load(cls, filename):
        vidcap = cv2.VideoCapture(str(filename))
        success, image = vidcap.read()
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        frames = []
        while success:
            frame = Frame(image)
            frames.append(frame)
            success, image = vidcap.read()
        return cls(frames, fps)

    def __getitem__(self, frame_number):
        return self.frames[frame_number]

    def append(self, frame: "Frame"):
        self.frames.append(frame)

    def view(self):
        ms_per_frame = int(1000 / self.fps)
        for frame in self.frames:
            cv2.imshow("window-name", frame.image)
            # Press Q on keyboard to  exit
            if cv2.waitKey(ms_per_frame) & 0xFF == ord("q"):
                break

    def save(self, filename, overwrite=True):
        height, width, layers = self.frames[0].image.shape
        size = (width, height)
        fps = self.fps
        # check if filename exists?
        out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*"mp4v"), fps, size)
        for f in self.frames:
            # writing to a image array
            out.write(f.image)

        out.release()


def detect_movement(video: Video):
    """detect and draw a box around the largets moving object in a video
    extracts coordiates of bounding box and timestamps
    """
    prev_frame_gray = None
    grays = []
    threshs = []
    movement = []
    with_rectangle = []
    frame: Frame
    for i, frame in enumerate(video):
        frame_gray = frame.gray()
        grays.append(frame_gray)
        if prev_frame_gray is None:
            prev_frame_gray = frame_gray
        diff = frame_gray.absdiff(prev_frame_gray)
        thresh = diff.threshold()
        largest_contour = thresh.find_largest_contour()
        prev_frame_gray = frame_gray
        if largest_contour is not None:
            threshs.append(thresh)
            box = frame.contour_summary(largest_contour)
            box["frame_number"] = i
            movement.append(box)
            rectangle_frame = frame.add_rectangle_from_contour(largest_contour)
            with_rectangle.append(rectangle_frame)
    # add rectangle to frames?
    movement = pd.DataFrame(movement)
    video_with_rect = Video(with_rectangle, video.fps)
    grays = Video(grays, video.fps)
    threshs = Video(threshs, video.fps)
    return movement, video_with_rect, grays, threshs


loc = []


def on_mouse(event, x, y, flags, param):
    global loc
    if event == cv2.EVENT_LBUTTONDOWN:
        # draw circle here (etc...)
        print(f"{x=}, {y=}")
        print(loc)
        loc.append((x, y))


def calibrate_distance(video: Video, i_frame=0):
    """sets a scale on the video based on a know distance in a fixed mage"""
    # get a frame from the video (first frame?)
    frame: Frame = video[i_frame]
    cv2.namedWindow("calibration")
    cv2.setMouseCallback("calibration", on_mouse)
    while len(loc) < 2:
        cv2.imshow("calibration", frame.image)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
        if len(loc) > 1:
            cv2.destroyAllWindows()
            break
        # show points on image + line
        # press key when done?
    print(loc)
    d = math.dist(loc[0], loc[1])
    print(f"Distance = {d} pixels")
    # actual_distance = typer.prompt("What's the actual disatnce?")
    # ask user to click on calibration points
    # calib["x1"] = x1
    # calib["x2"] = x2
    # calib["y1"] = y1
    # calib["y2"] = y2
    # calib["dist_image"] = math.dist([x1, y1], [x2, y2])

    # # ask user for disatnce between points

    # calib["distance"] = d_real
    # calib["scale"] = calib["distance"] / calib["dist_image"]

    # self.calib = calib


def estimate_speed(self):
    """estimate the speed of the largest moving object(s)?"""
    pass
