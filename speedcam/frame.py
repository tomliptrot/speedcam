import cv2


class Frame:
    def __init__(self, image):
        self.image = image

    def absdiff(self, other)-> "Frame":
        d = cv2.absdiff(self.image, other.image)
        return Frame(d)

    def threshold(self, threshold=10) -> "Frame":
        _, thresh = cv2.threshold(self.image, threshold, 255, cv2.THRESH_BINARY)
        # This dilates with two iterations
        thresh = cv2.dilate(thresh, None, iterations=5)
        return Frame(thresh)

    def gray(self) -> "Frame":
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        return Frame(gray)

    def add_rectangle(self, pt1, pt2, colour = (0, 255, 0), thickness=10) -> "Frame":
        image = self.image.copy()
        cv2.rectangle(image, pt1, pt2, colour, thickness)
        return Frame(image)

    def add_rectangle_from_contour(self, contour, colour = (0, 255, 0), thickness=10) -> "Frame":
        x,y,w,h = cv2.boundingRect(contour)
        return self.add_rectangle((x, y), (x + w, y + h), colour, thickness)

    def find_contours(self):
        contours, hierarchy = cv2.findContours(self.image,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        return contours

    def find_largest_contour(self, min_area = 10000):
        contours = self.find_contours()
        biggest_size = min_area
        largest_contour = None

        for i,cntr in enumerate(contours):
            area = cv2.contourArea(cntr)
    
            if area  > biggest_size:
                largest_contour = cntr
                biggest_size = area 
        return largest_contour

    def contour_summary(self, contour):
        summary = {}

        x, y, w, h = cv2.boundingRect(contour)
        summary["area"] = cv2.contourArea(contour)
        summary["x"] = x
        summary["y"] = y
        summary["w"] = w
        summary["h"] = h

        moments = cv2.moments(contour)
        summary["centre_x"] = int(moments["m10"] / moments["m00"])
        summary["centre_y"] = int(moments["m01"] / moments["m00"])
        # else:
        # with_rectangle.append(frame)
        return summary



