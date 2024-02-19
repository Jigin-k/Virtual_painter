import cv2
import HandTrackingModule as htm
import numpy as np
import time

cap = cv2.VideoCapture(0)
detector = htm.handDetector()

draw_color = (0,0,255)

img_canvas = np.zeros((720,1280,3),np.uint8)

p_time = 0


while True:
    success, frame = cap.read()
    frame = cv2.resize(frame,(1280,720))
    frame = cv2.flip(frame, 1)
    cv2.rectangle(frame,pt1=(40,10),pt2=(250,100),color=(0,255,0),thickness=-10)
    cv2.rectangle(frame,pt1=(260,10),pt2=(470,100),color=(255,0,0),thickness=-10)
    cv2.rectangle(frame,pt1=(480,10),pt2=(690,100),color=(0,0,255),thickness=-10)
    cv2.rectangle(frame,pt1=(700,10),pt2=(910,100),color=(255,255,0),thickness=-10)
    cv2.rectangle(frame,pt1=(920,10),pt2=(1240,100),color=(255,255,255),thickness=-10)
    cv2.putText(frame,text='Eraser',org=(1000,75),fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,fontScale=2,color=(0,0,0),thickness=3)    

    frame= detector.findHands(frame) 

    lmlist =detector.findPosition(frame)

    if len(lmlist)!=0:
      x1,y1 = lmlist[8][1:]
      x2,y2 = lmlist[12][1:]

      #print(x1,y1,x2,y2)
      

      fingers = detector.fingersUp()
      #print(fingers)
      
      if fingers[1] and fingers[2]:
         #print('selection_mode')
         xp,yp = 0,0

         if y1<100:

            if 40<x1<240:
               draw_color = (0,255,0)
               #print('green')
            elif 250<x1<470:
               draw_color = (255,0,0)
               #print('blue')   
            elif 480<x1<690:
               draw_color = (0,0,255)
               #print('red')
            elif 700<x1<910:
               draw_color=(255,255,0)
               #print('skyblue') 
            elif 920<x1<1240:
               draw_color=(0,0,0)
               #print('eraser')        
         
         
         
         cv2.rectangle(frame,(x1,y1),(x2,y2),draw_color,thickness=cv2.FILLED)


      if (fingers[1] and not fingers[2]):
         #print('drawing_mode')


         
         cv2.putText(frame,"Drawing Mode",(1000,650),fontFace=cv2.FONT_HERSHEY_COMPLEX,color = (0,255,255),fontScale=1,thickness=3)
         cv2.circle(frame,(x1,y1),15,draw_color,thickness=-1)

         if xp==0 and yp==0:

            xp=x1
            yp=y1
         
         if draw_color== (0,0,0):
            cv2.line(frame,(xp,yp),(x1,y1),color=draw_color,thickness=10)
            cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=50)
         else:
            cv2.line(frame,(xp,yp),(x1,y1),color=draw_color,thickness=10)   
            cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=10)

         xp,yp = x1,y1   


    #merging 2 Canvas

    img_gray = cv2.cvtColor(img_canvas,cv2.COLOR_BGR2GRAY)

    # thresh Inverse

    thresh,img_inv = cv2.threshold(img_gray,20,255,cv2.THRESH_BINARY_INV)

    img_inv = cv2.cvtColor(img_inv,cv2.COLOR_GRAY2BGR)

    frame = cv2.bitwise_and(frame,img_inv)
    frame = cv2.bitwise_or(frame,img_canvas)

    frame = cv2.addWeighted(frame,1,img_canvas,0.5,0)

   
    #calculating FPS

    c_time = time.time()
    

    fps = 1 / (c_time - p_time)

    p_time = c_time

    cv2.putText(frame, str(int(fps)), (50,150),cv2.FONT_HERSHEY_COMPLEX,5, (0,255,0),thickness=4)



    cv2.imshow('video_capture',frame)
   #  cv2.imshow('canvas',img_canvas)
   #  cv2.imshow('grey',img_inv)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()