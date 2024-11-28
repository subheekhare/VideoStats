import numpy as np
import cv2 

def frame_classification(imagepath):
    if imagepath is not None:
        img_hsv = cv2.cvtColor(imagepath, cv2.COLOR_BGR2HSV)
        avg_h, avg_s, avg_v = cv2.mean(img_hsv)[:3]  # Ignore alpha channel
    if np.all((np.round(avg_v) <=30) ):
        classification= "N"
    elif np.all((np.round(avg_v)>30) & (np.round(avg_v) <= 135)):
        classification= "E"
    elif np.all((np.round(avg_v)>135 )):
        classification= "D"
    else:
        classification= "T"    
    # print(np.round(avg_h), np.round(avg_s) , np.round(avg_v))#, classification)
    return classification

video_name="Day to Night Afternoon Timelapse - Wind Smoke Trees Clouds And Sky January 2020.mp4"
cap=cv2.VideoCapture(video_name)
fr_len=int(cap.get(cv2.CAP_PROP_FRAME_COUNT ))
counter=[]
brightn = 0
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        # print("Can't receive frame (stream end?). Exiting ...")
        break
    else:
        #---------------Value Thresholding ---------------#
        brightn = frame_classification(frame)
        counter.append(brightn)
   # cv2.imshow('frame', frame)
    # if cv2.waitKey(1) == ord('q'):
    #     break
day_per = np.round(counter.count('D')*100/fr_len, 2)
evening_per= np.round(counter.count('E')*100/fr_len, 2)
night_per= np.round(counter.count('N')*100/fr_len, 2)

if counter.count('D')>0:
    message = f'Day Share: {day_per}%'
if counter.count('E')>0:
    message = message + f', Evening Share: {evening_per}%'     
if counter.count('N')>0:
    message = message + f', Night Share: {night_per}%'     
    
print(f'Total Frame: {fr_len}, file name: {video_name} Stats: {message}')
cap.release()
# cv2.destroyAllWindows()