#include <iostream>
#include <iomanip>
#include <opencv2/core.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

#include "findcorners.h"
#include "colorinpicture.h"


int main()
{
//  Test Image
    cv::String path = "/home/erkja19/SDU/Vision/img/testLooking/";
    cv::Mat image = cv::imread(path+"8new.jpg");

//  Variabler
    bool print = 1;
    double maxCorners = 200;
    ColorInPicture colorInPic;
    FindCorners corners;

//  Isolated the red in the photo
    cv::Mat colorCvt = colorInPic.colorCvt(image);
    cv::Mat gausImg = colorInPic.gausBlur(colorCvt);
    cv::Mat foundColor = colorInPic.colorFind(image, gausImg);
    cv::Mat colorCorners = colorInPic.fourCornersColor(colorCvt);

//  Finding the corners and Making the square
    cv::Mat grayImg = corners.grayCvt(foundColor);
    std::vector<cv::Point> foundCorners = corners.cornerFinder(grayImg, maxCorners);
    //std::vector<cv::Point> fourRightCorners = corners.fourCorners(foundCorners);
    std::vector<cv::Point> fourRightCorners = corners.findingExtPoints(foundCorners);
    for(unsigned int i = 0; i < fourRightCorners.size(); i++)
    {
        corners.myCircle(foundColor,fourRightCorners[i]);
    }
    std::cout << "All corners" << fourRightCorners << std::endl;


//  Show Images
    if(print)
    {
    cv::namedWindow( "Image",cv::WINDOW_AUTOSIZE);
    cv::imshow("Image", image);
    cv::waitKey(0);
    cv::imshow("Color in Picture", foundColor);
    cv::waitKey(0);/*
    cv::imshow("Color in Picture", foundColor);
    cv::waitKey(0);*/
    }
    return 0;
}
