#ifndef COLORINPICTURE_H
#define COLORINPICTURE_H

#include <opencv2/core.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

class ColorInPicture
{
public:
    ColorInPicture();

    cv::Mat colorCvt(cv::Mat img);
    cv::Mat gausBlur(cv::Mat imgCvt);
    cv::Mat colorFind(cv::Mat img, cv::Mat imgGaus);
    cv::Mat fourCornersColor(cv::Mat imgCvt);

private:
    cv::Mat img,imgCvt,imgGaus,mask,result;
    cv::Scalar colorRed = cv::Scalar(0,0,0);
    cv::Size kernelSize = {3,3};

};

#endif // COLORINPICTURE_H
