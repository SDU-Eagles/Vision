sudo apt install cmake gcc g++ libavcodec-dev libavformat-dev libswscale-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev python3-dev python3-numpy libgtk-3-dev libpng-dev libjpeg-dev libopenexr-dev libtiff-dev libwebp-dev git libcblas-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4  libqt4-test
pip3 install --upgrade numpy
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
cd opencv
mkdir build
cd build
cmake -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules ../
make -j 4
sudo make install
