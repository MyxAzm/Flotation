import cv2
import numpy as np

image = cv2.imread("img.png")


blur = cv2.medianBlur(image, 5)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray,180,255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

min_area = 0.1
white_dots = []
for c in cnts:
   area = cv2.contourArea(c)
   if area > min_area:
      cv2.drawContours(image, [c], -1, (36, 255, 12), 1)
      white_dots.append(c)

print("White Dots count is:",len(white_dots))
cv2.imshow('image', image)
cv2.waitKey()


def getVideo():
    capture = cv2.VideoCapture("video.mp4")
    percent = 20
    while (capture.isOpened()):
        ret, frame =capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        frame_re = cv2.resize(frame, dim)
        # cv2.imshow('frame', frame)
        cv2.imshow('Frame', gray)
        if cv2.waitKey(33)&0xFF == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows()




