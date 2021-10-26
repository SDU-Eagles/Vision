#include <iostream>
#include <opencv2/core.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

int main()
{
    cv::String path = "/home/erkja19/SDU/Vision/img/testLooking/";
    cv::Mat image = cv::imread(path+"13new.jpg");

    cv::namedWindow( "Display window",cv::WINDOW_AUTOSIZE);
    cv::imshow("Display window",image);
    cv::waitKey(0);

    cv::Mat imageColorCvt;
    cv::cvtColor(image,imageColorCvt,cv::COLOR_BGR2HSV);

    cv::Mat imageGaus;
    cv::GaussianBlur(imageColorCvt,imageGaus,cv::Size(3,3),2,2);

    //lower[155,25,0];
    //upper[179,255,255];

    //cv::inRange(lower,cv::Scalar(155,25,0),cv::Scalar(156,26,1),lower);
    //cv::inRange(upper,cv::Scalar(179,255,255),cv::Scalar(180,255,255),upper);


    cv::Mat mask;
    cv::inRange(imageGaus,cv::Scalar(0,50,0),cv::Scalar(180,150,255),mask);


    cv::Mat result;
    cv::bitwise_and(image,image,result,mask=mask);

    cv::imshow("mask",mask);
    cv::waitKey(0);

    cv::imshow("result",result);
    cv::waitKey(0);

    return 0;
}
