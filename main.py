import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,100)

def empty(a):
    pass



kernel = np.ones((5,5),np.uint8)

canvas = None
x1,y1 = 0,0


cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("Hue Min","TrackBars",37,179,empty)
cv2.createTrackbar("Hue Max","TrackBars",77,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",167,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",255,255,empty)
cv2.createTrackbar("Val Min","TrackBars",71,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)

cv2.namedWindow('image',cv2.WINDOW_NORMAL)

noiseth = 500


while True:
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")





    success, img = cap.read()
    img = cv2.flip(img,1)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)
    mask = cv2.erode(mask,kernel,iterations=1)
    mask = cv2.dilate(mask,kernel,iterations=2)
    imgResult = cv2.bitwise_and(img,img,mask=mask)
    mask_3 = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)

    if canvas is None:
        canvas = np.zeros_like(img)

    contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    if contours and cv2.contourArea(max(contours,key = cv2.contourArea)) > noiseth:
        c = max(contours,key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,25,255),2)



        if x1 == 0 and y1 == 0:
            x1, y1 = x, y
        else:
            canvas = cv2.line(canvas,(x1,y1),(x,y),[0,255,0],4)
            x1,y1 = x,y
    else:
        x1,y1 = 0,0

    img = cv2.add(img,canvas)

    stacked = np.hstack((canvas,img))

    k = cv2.waitKey(1) & 0XFF
    if k == ord('c'):
        canvas = None

    cv2.imshow('image',img)

    #cv2.imshow("Virtual Draw",cv2.resize(stacked,None,fx=0.4,fy=0.4))
    #cv2.imshow("imgHSV",imgHSV)
    #cv2.imshow("Mask",mask)


    if cv2.waitKey(1) & 0xFF == ord('s'):
        thearray = [[h_min, s_min, v_min], [h_max, s_max, v_max]]
        np.save('penval', thearray)
        break