#include "colorinpicture.h"

ColorInPicture::ColorInPicture(){}

cv::Mat ColorInPicture::colorCvt(cv::Mat img)
{
    cv::Mat imgCvtHSV;
    cv::cvtColor(img,imgCvt,cv::COLOR_BGR2HSV);
    return imgCvt;
}

cv::Mat ColorInPicture::gausBlur(cv::Mat imgCvt)
{
    cv::Mat imgGaus;
    cv::GaussianBlur(imgCvt, imgGaus, kernelSize, 2, 2);
    return imgGaus;
}

cv::Mat ColorInPicture::colorFind(cv::Mat img, cv::Mat imgGaus)
{
    cv::Mat mask;
    cv::Mat result;
    cv::inRange(imgGaus, cv::Scalar(0,50,0), cv::Scalar(180,150,255),mask);
    cv::bitwise_and(img, img, result, mask=mask);
    return result;
}

cv::Mat ColorInPicture::fourCornersColor(cv::Mat imgCvt)
{
    int iLowH = 160; int iHighH = 190;
    int iLowS = 7; int iHighS = 255;
    int iLowV = 60;  int iHighV = 255;
    int iLastX = -1; int iLastY = -1;
    cv::Mat imgThresholded;

    cv::inRange(imgCvt,cv::Scalar(iLowH, iLowS, iLowV), cv::Scalar(iHighH, iHighS, iHighV),imgThresholded);
//  morphological opening
    cv::erode(imgThresholded,imgThresholded,cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(3, 3)));
    cv::dilate(imgThresholded,imgThresholded,cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(3, 3)));
//  morphological closing
    cv::dilate(imgThresholded,imgThresholded,cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(3, 3)));
    cv::erode(imgThresholded,imgThresholded,cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(3, 3)));

    cv::Moments oMoments = cv::moments(imgThresholded);

    double dArea = oMoments.m00;
    double dM01 = oMoments.m01;
    double dM10 = oMoments.m10;

    if(dArea > 10000)
    {
        int posX = dM10 / dArea;
        int posY = dM01 / dArea;

        iLastX = posX;
        iLastY = posY;
    }


    return imgThresholded;
}
