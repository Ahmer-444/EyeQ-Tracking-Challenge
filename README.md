# EyeQ-Tracking-Challenge
This repository is intended for EyeQ's AI Challenge for person detection and tracking.

## Available Input
Input video can be downloaded from here.
https://bit.ly/2L8hFGE

## Desired Output
A .txt file having the class of relevant object/objects following the predicted bounding box coordinates. Each row in txt file will correspond to a frame in video.
```
class1 xmin1 ymin1 xmax1 ymax1 class2 xmin2 ymin2 xmax2 ymax2 ...
1 1487 732 1775 1069 5 1009 140 1137 482 ...
```

## Developed Approach
I have used deep learning approach Faster RCNN with Feature Extractor architecture of Resnet-50. In order to train a model that can track the desired objects, I need annotations for these objects (persons) in Pascal xml format. 
So here are few steps that I have followed to achieve desired results.

Performance Accuracy Achieved: 95%

### Ground Truth Visualization & Data Preperation
First of all, ground truth has been mapped on to the input video to visualize the ground truth that has been marked. Beside that an algorthm has been written to accurately write bounding box coordinates in .txt file in desired format. Furthermore, developed a utility that can create annoations (xmls) from an image and GT information `generate_xml.py`.
To run and get described output, run the script as:

	`python3 mark_GT.py` 

	Output: annotations/ , images/ , res_masan_2.mp4 (GT visualization)

### System Configuration
Tensorflow's Object Detection API has been used to train the desired architecture. I have installed the requirements for the API and configure the machine with CUDA, Cudnn libraries for GPU acceleration. To get more details, please have a look at [Tensorflow's Object Detection API Instructions](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md)

### Training
Now, we have configured our system and have necessary files to start training for person tracker. To run the training job procedure, please visit [training documentation](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/running_locally.md)

### Trained Model
Please download the trained model from [here](https://drive.google.com/open?id=1uvKB4GIbf8_JJLPIj9SYs3AZaQOgYBmu) and place it in the ROOT project directory. It will be named as `output_inference_graph.pb`

### Video Inference
Run inference on the input video as
	`python3 person_tracker.py -i INPUT_VIDEO_PATH.mp4 -o OUTPUT_VIDEO_PATH.mp4`
	Output: predictions.txt (predicted bboxes and objects), OUTPUT_VIDEO_PATH.mp4 (contains visualization of tracking)

### Evaluation
Run the evaluation script as follows:
	`./run_accuracy_test` or simply type `python3 eval_tracker.py -f txts/predictions.txt -g txts/masan_2_gt.txt`

Output
`
ground_truth/frames: {1: 18832, 2: 4050, 3: 10613, 4: 9402, 5: 4925, 6: 3681, 7: 11934}
Person accuracy 1 0.9929906542056075
Person accuracy 2 0.9511111111111111
Person accuracy 3 0.9234900593611608
Person accuracy 4 0.8992767496277387
Person accuracy 5 0.9723857868020305
Person accuracy 6 0.967400162999185
Person accuracy 7 0.9616222557399028
Tracking accuracy 0.9526109685495339
`

#### Pascal Evaluation Metrics
Pascal's performance metrics have been computed for the current system to see how well our system is behaving. The graphs to these metrics have been placed under directory `accuracy_metrics_graphs/`.
The type of graphs are:
1. Loss Graph - (close to 0)
2. Performance by Category - AP @ 0.5IoU (close to 1)

Please visit [Pascal Performance Metrics](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/evaluation_protocols.md) for more details.