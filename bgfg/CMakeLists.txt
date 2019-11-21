cmake_minimum_required(VERSION 2.8)
set(OPENCV_CPP_SAMPLES_REQUIRED_DEPS
  opencv_core
  opencv_imgproc
  opencv_flann
  opencv_imgcodecs
  opencv_videoio
  opencv_highgui
  opencv_ml
  opencv_video
  opencv_objdetect
  opencv_photo
  opencv_features2d
  opencv_calib3d
  opencv_stitching
  ${OPENCV_MODULES_PUBLIC}
  ${OpenCV_LIB_COMPONENTS})
#ocv_check_dependencies(${OPENCV_CPP_SAMPLES_REQUIRED_DEPS})

project(cpp_bgfg)

#ocv_include_modules_recurse(${OPENCV_CPP_SAMPLES_REQUIRED_DEPS})

add_executable(bgfg_segm bgfg_segm.cpp)
target_link_libraries( bgfg_segm ${OpenCV_LIBS} ${OPENCV_CPP_SAMPLES_REQUIRED_DEPS} )