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

//  Isolated the red in the photo
    cv::Mat imageColorCvt;
    cv::cvtColor(image,imageColorCvt,cv::COLOR_BGR2HSV);

    cv::Mat imageGaus;
    cv::GaussianBlur(imageColorCvt,imageGaus,cv::Size(3,3),2,2);

    cv::Mat mask;
    cv::inRange(imageGaus,cv::Scalar(0,50,0),cv::Scalar(180,150,255),mask);

    cv::Mat result;
    cv::bitwise_and(image,image,result,mask=mask);

    cv::imshow("mask",mask);
    cv::waitKey(0);
    cv::imshow("result",result);
    cv::waitKey(0);

//
    int thresh = 200;
    cv::Mat gray, dst, dstNorm, dstNormScaled;
    cv::cvtColor(result,gray,cv::COLOR_BGR2GRAY);

    dst = cv::Mat::zeros(result.size(),CV_32FC1);

    cv::cornerHarris(gray,dst,7,5,0.05);

    cv::normalize(dst,dstNorm,0,255,cv::NORM_MINMAX,CV_32FC1,cv::Mat());
    cv::convertScaleAbs(dstNorm,dstNormScaled);

    for( int j = 0; j < dstNorm.rows ; j++ )
    {
        for( int i = 0; i < dstNorm.cols; i++ )
        {
            if( (int) dstNorm.at<float>(j,i) > thresh )
            {
               cv::circle( dstNormScaled, cv::Point( i, j ), 5,  cv::Scalar(0), 2, 8, 0 );
            }
        }
    }
    std::cout << dstNormScaled << std::endl;
    cv::namedWindow( "corners_window",cv::WINDOW_AUTOSIZE);
    cv::imshow("corners_window",dstNormScaled);
    cv::waitKey(0);


    return 0;
}
