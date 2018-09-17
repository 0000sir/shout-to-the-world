#! /bin/bash

gcc -shared -o libmog2.so -fPIC ./mog2.cpp -lopencv_core -lopencv_highgui -lopencv_objdetect -lopencv_imgproc -lopencv_features2d -lopencv_ml -lopencv_calib3d -lopencv_contrib -lopencv_video

