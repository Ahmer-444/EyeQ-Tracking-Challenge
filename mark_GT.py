import cv2
import time
import os

from generate_xml import write_xml

"""
This Python utility draw Ground Truth bounding boxes on a video using GT.txt and create annnoations (xml) for training purposes.
"""

def VideoRecInit(VID_RECORD_PATH,WIDTH,HEIGHT):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    videowriter = cv2.VideoWriter(VID_RECORD_PATH, fourcc, 30.0, (WIDTH,HEIGHT))
    return videowriter


read_fname = 'masan_2_gt.txt'
write_fname = 'predicted_masan_2_gt.txt'
VideoPath = 'masan_2.mp4'
VID_RECORD_PATH =  "res_" + VideoPath


with open(read_fname) as f:
    gt_info = f.readlines()

# you may also want to remove whitespace characters like `\n` at the end of each line
gt_info = [x.strip() for x in gt_info]
gt_list = [tuple(s for s in i.split(' ')) for i in gt_info]


cap = cv2.VideoCapture(VideoPath)
while not cap.isOpened():
    cap = cv2.VideoCapture(VideoPath)
    cv2.waitKey(1000)
    print ("Wait for the header")

flag, image = cap.read()
#image = imutils.rotate_bound(image, 90)
(ht,wd,_) = image.shape
videowriter = VideoRecInit(VID_RECORD_PATH,wd,ht)

folder = 'images'
savedir = 'annotations'
path = os.path.abspath(folder)

if not os.path.isdir(folder):
    os.mkdir(folder)
if not os.path.isdir(savedir):
    os.mkdir(savedir)

frame_no = -1
while True:
    start_time = time.time()
    frame_no +=1    
    print (frame_no)
    flag, image = cap.read()
    orig_image = image.copy()
    gt_candidate = gt_list[frame_no]
    
    if len(gt_candidate) < 5:
    	print ("No Person!!!")
    	f = open(write_fname,'a') 
    	f.write('\n')
    	continue
    else:
        print (gt_candidate)
        num_persons = int (len(gt_candidate) / 5)
        objects = []
        bbox = []

        for i in range(num_persons):
        	pid = gt_candidate[0 + (i*5)]
        	xmin = int(gt_candidate[1 + (i*5)])
        	ymin = int(gt_candidate[2 + (i*5)])
        	xmax = int(gt_candidate[3 + (i*5)])
        	ymax = int(gt_candidate[4 + (i*5)])

        	pt1 = (xmin,ymin)
        	pt2 = (xmax,ymax)
        	cv2.rectangle(image, pt1, pt2, (255, 255, 0), 3)
        	loc = (xmin,ymin-20)
        	cv2.putText(image, pid, loc , cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,255), 6)
        	
        	#The frame is ready and already captured
        	# cv2.namedWindow('video', cv2.WINDOW_NORMAL)
        	# cv2.imshow('video', image)
        	# if cv2.waitKey(1) & 0xFF == ord('q'):
        	# 	break
        	videowriter.write(image)

        	bbox.append((xmin,ymin,xmax,ymax))
        	objects.append(str(pid))

        # 	f = open(write_fname,'a')
        # 	txt = pid + ' ' + str(xmin) + ' ' + str(ymin) + ' ' + str(xmax) + \
        # 	 ' ' + str(ymax) + ' '
        # 	f.write(txt)
        # f.write('\n')
        
        filename = 'frame_no_' + '{0:05}'.format(frame_no) + '.jpg'
        write_xml(folder, orig_image, filename, path, objects, bbox, savedir)
        print("--- %s seconds ---" % (time.time() - start_time))


cap.release()
videowriter.release()
#cv2.destroyAllWindows()
