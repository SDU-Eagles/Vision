#ifndef FINDCORNERS_H
#define FINDCORNERS_H

#include <iostream>
#include <opencv2/core.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

class FindCorners
{
public:
    FindCorners();

    void myCircle(cv::Mat img, cv::Point center);
    cv::Mat grayCvt(cv::Mat imgColor);
    std::vector<cv::Point> cornerFinder(cv::Mat grayImg, double maxCorners);
    std::vector<cv::Point> fourCorners(std::vector<cv::Point> corners);
    std::vector<cv::Point> fourCorners2(std::vector<cv::Point> corners);
//    std::vector<cv::Point> fourCornersColor(std::vector<cv::Point> corners);
    std::vector<cv::Point> findingExtPoints(std::vector<cv::Point> pts);

private:
    cv::Mat allCorners, imgColor, grayImg, img;
    double maxCorners;
    double lowestX = corners.at(0).x;
    double lowestY = corners.at(0).y;
    double highstX = corners.at(0).x;
    double highstY = corners.at(0).y;
    std::vector<cv::Point> corners, fourRightCorners;
    cv::Point cornerLowestX, cornerLowestY, cornerHighstX, cornerHighstY, center;
};

#endif // FINDCORNERS_H
