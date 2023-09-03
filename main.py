import cv2
import numpy as np
import math
import psycopg2



# высчитывает радиус
def getRadius(area):

    radius = round(math.sqrt(area / math.pi))

    return radius

# выдает контуры
def getContours(image):

    blur = cv2.medianBlur(image, 5)
    thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    return cnts

# находит окружности
def detectBubbles(image):

    min_area = 0.1
    bubbles_count = 0
    max_radius = 0
    cnts = getContours(image)
    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_area:
            bubbles_count = bubbles_count + 1
            moment = cv2.moments(c)
            if moment['m00'] != 0:
               cx = int(moment['m10']/moment['m00'])
               cy = int(moment['m01']/moment['m00'])
               radius = getRadius(area)
               cv2.circle(image, (cx, cy), radius, (0, 0, 255), -1)

               if radius > max_radius:
                   max_radius = radius
    return {"bubbles_count": bubbles_count, "max_radius": max_radius}

def getVideo():
    con = psycopg2.connect(dbname='DataBaseBubbles', user='postgres', password='1996', host='127.0.0.1')
    capture = cv2.VideoCapture("video.mp4")
    percent = 20
    while (capture.isOpened()):

        cur = con.cursor()

        datas = {
            "bubbles_count": "",
            "bubbles_velocity": 5.5,
            "max_radius": "",
            "time": "12:00:00"
        }

        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        frame_re = cv2.resize(frame, dim)
        data = detectBubbles(gray)
        datas["bubbles_count"] = data["bubbles_count"]
        datas["max_radius"] = data["max_radius"]
        keys = datas.keys()
        sql = "INSERT INTO public.'Bubbles' (" + ", ".join(datas.keys()) + ") VALUES (" + ", ".join(["%("+c+")s" for c in datas]) + ")"
        cursor = con.cursor()
        cursor.execute(sql, datas)
        # cv2.imshow('frame', gray)
        con.commit()

        if cv2.waitKey(33)&0xFF == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows()
    con.close()


getVideo()
