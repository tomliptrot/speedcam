import math
import cv2
from frame import Frame
class Video:
    def __init__(self, frames: "list[Frame]", fps=30):
        self.frames = frames
        self.fps = fps

    @classmethod
    def load(cls, filename):
        vidcap = cv2.VideoCapture(filename)
        success, image = vidcap.read()
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        frames = []
        while success:  
            frame = Frame(image)
            frames.append(frame)
            success, image = vidcap.read()
        return cls(frames, fps)

    def __getitem__(self,frame_number):
        return self.frames[frame_number]
            
    def view(self):
        for frame in self.frames:
            cv2.imshow('window-name', frame.image)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    def save(self, filename):
        height, width, layers = self.frames[0].image.shape
        size = (width,height)
        fps = self.fps
        #check if filename exists?
        out = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
        for f in self.frames:
            # writing to a image array
            out.write(f.image)

        out.release()

    def calibrate_distance(self):
        """sets a scale on the video based on a know distance in a fixed mage
        """
        calib = {}
        #get a frame from the video (first frame?)

        #show it

        #ask user to click on calibration points
        calib['x1'] = x1
        calib['x2'] = x2
        calib['y1'] = y1
        calib['y2'] = y2
        calib['dist_image'] = math.dist([x1, y1], [x2, y2])

        #ask user for disatnce between points

        calib['distance'] = d_real
        calib['scale'] = calib['distance'] / calib['dist_image'] 

        self.calib = calib

    def detect_moving_object(self):
        """detect and draw a box around the largets moving object in a video
        extracts coordiates of bounding box and timestamps
        """
        prev_frame_gray = None
        grays = []
        threshs = []
        movement = []
        with_rectangle = []
        frame: Frame
        for i, frame in enumerate(self):
            frame_gray = frame.gray()
            grays.append(frame_gray)
            if prev_frame_gray is None:
                prev_frame_gray = frame_gray
            diff = frame_gray.absdiff(prev_frame_gray)
            thresh = diff.threshold()
            threshs.append(thresh)
            largest_contour = thresh.find_largest_contour()

            prev_frame_gray = frame_gray
            out = {}
            out['frame_number'] = i
            out['largest_contour'] = largest_contour 
            if largest_contour is not None:
                x,y,w,h = cv2.boundingRect(largest_contour)
                out['x'] = x
                out['y'] = y
                out['w'] = w
                out['h'] = h
                with_rectangle.append(frame.add_rectangle_from_contour(largest_contour))
            else:
                with_rectangle.append(frame)
            movement.append(out)
        #add rectangle to frames?
        
        return movement, Video(with_rectangle, self.fps), Video(grays, self.fps), Video(threshs, self.fps)

    def estimate_speed(self):
        """estimate the speed of the largest moving object
        """
        pass


vid = Video.load('data/motorbike.mp4')
movement, with_rectangle, grays, threshs = vid.detect_moving_object()
with_rectangle.view()
