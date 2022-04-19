#include "findcorners.h"

FindCorners::FindCorners(){}

void FindCorners::myCircle(cv::Mat img, cv::Point center)
{
    cv::circle(img, center, 10, cv::Scalar(100,255,0),2);
}

cv::Mat FindCorners::grayCvt(cv::Mat imgColor)
{
    cv::Mat imgCvtGray;
    cv::cvtColor(imgColor, imgCvtGray, cv::COLOR_BGR2GRAY);
    return imgCvtGray;
}

std::vector<cv::Point> FindCorners::cornerFinder(cv::Mat grayImg, double maxCorners)
{
    cv::goodFeaturesToTrack(grayImg, corners, maxCorners, 0.01, 1);
    std::cout << "Corners found: " << corners.size() << std::endl;
    return corners;
}

std::vector<cv::Point> FindCorners::fourCorners(std::vector<cv::Point> corners)
{
    for(unsigned int i = 0; i < corners.size(); i++)
    {
        if(lowestX > corners.at(i).x)
        {
            lowestX = corners.at(i).x;
            cornerLowestX = corners.at(i);
        }
    }
    for(unsigned int i = 0; i < corners.size(); i++)
    {
        if(lowestY > corners.at(i).y)
        {
            lowestY = corners.at(i).y;
            cornerLowestY = corners.at(i);
        }
    }
    for(unsigned int i = 0; i < corners.size(); i++)
    {
        if(highstX < corners.at(i).x)
        {
            highstX = corners.at(i).x;
            cornerHighstX = corners.at(i);
        }
    }
    for(unsigned int i = 0; i < corners.size(); i++)
    {
        if(highstY < corners.at(i).y)
        {
            highstY = corners.at(i).y;
            cornerHighstY = corners.at(i);
        }
    }
    std::cout << "Lowest x corner værdi: " << cornerLowestX << std::endl; // Should be around [620,660]
    std::cout << "Lowest y corner værdi: " << cornerLowestY << std::endl; // Should be around [620,660]
    std::cout << "Highst x corner værdi: " << cornerHighstX << std::endl; // Should be around [620,660]
    std::cout << "Highst y corner værdi: " << cornerHighstY << std::endl; // Should be around [620,660]

    fourRightCorners.push_back(cornerLowestX);
    fourRightCorners.push_back(cornerLowestY);
    fourRightCorners.push_back(cornerHighstX);
    fourRightCorners.push_back(cornerHighstY);

    return fourRightCorners;
}

std::vector<cv::Point> FindCorners::fourCorners2(std::vector<cv::Point> corners)
{
    for(unsigned int i = 0; i < corners.size(); i++)    // Virker (?)
    {
        if(lowestX > corners.at(i).x || lowestY > corners.at(i).y || (lowestX > corners.at(i).x && lowestY > corners.at(i).y))
        {
            lowestX = corners.at(i).x;
            lowestY = corners.at(i).y;
            cornerLowestX = corners.at(i);
        }
    }
    for(unsigned int i = 0; i < corners.size(); i++)    // Virker ikke :(
    {
        if(lowestX > corners.at(i).x || highstY < corners.at(i).y || (lowestX > corners.at(i).x && highstY < corners.at(i).y))
        {
            lowestX = corners.at(i).x;
            highstY = corners.at(i).y;
            cornerHighstY = corners.at(i);
        }
    }
    for(unsigned int i = 0; i < corners.size(); i++)    // Virker ikke :(
    {
        if(highstX < corners.at(i).x || lowestY > corners.at(i).y || ( highstX < corners.at(i).x && lowestY > corners.at(i).y))
        {
            highstX = corners.at(i).x;
            lowestY = corners.at(i).y;
            cornerLowestY = corners.at(i);
        }
    }
    for(unsigned int i = 0; i < corners.size(); i++)    // Virker
    {
        if(highstX < corners.at(i).x || highstY < corners.at(i).y || (highstX < corners.at(i).x && highstY < corners.at(i).y))
        {
            highstX = corners.at(i).x;
            highstY = corners.at(i).y;
            cornerHighstX = corners.at(i);
        }
    }

    std::cout << "Lowest x corner værdi: " << cornerLowestX << std::endl; //
    std::cout << "Lowest y corner værdi: " << cornerLowestY << std::endl; //
    std::cout << "Highst x corner værdi: " << cornerHighstX << std::endl; //
    std::cout << "Highst y corner værdi: " << cornerHighstY << std::endl; //

    fourRightCorners.push_back(cornerLowestX);
    fourRightCorners.push_back(cornerLowestY);
    fourRightCorners.push_back(cornerHighstX);
    fourRightCorners.push_back(cornerHighstY);

    return fourRightCorners;
}

std::vector<cv::Point> FindCorners::findingExtPoints(std::vector<cv::Point> pts)
{
    cv::Point extLeft = *std::min_element(pts.begin(),pts.end(),[](const cv::Point& lhs, const cv::Point& rhs){return lhs.x < rhs.x;});
    cv::Point extRight = *std::max_element(pts.begin(),pts.end(),[](const cv::Point& lhs, const cv::Point& rhs){return lhs.x < rhs.x;});
    cv::Point extTop = *std::min_element(pts.begin(),pts.end(),[](const cv::Point& lhs, const cv::Point& rhs){return lhs.y < rhs.y;});
    cv::Point extBot = *std::max_element(pts.begin(),pts.end(),[](const cv::Point& lhs, const cv::Point& rhs){return lhs.y < rhs.y;});

    fourRightCorners.push_back(extLeft);
    fourRightCorners.push_back(extRight);
    fourRightCorners.push_back(extTop);
    fourRightCorners.push_back(extBot);

    return fourRightCorners;
}






