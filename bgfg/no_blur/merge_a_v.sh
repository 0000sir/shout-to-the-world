#! /bin/bash

ffmpeg -i fg_video.avi -i ../x-12.m4a -c:v copy -c:a copy fg_combine.avi
