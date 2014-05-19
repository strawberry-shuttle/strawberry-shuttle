//Based on: http://felix.abecassis.me/2011/09/opencv-morphological-skeleton/

#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "highgui.h"

#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char** argv)
{
    const char* filename = argc >= 2 ? argv[1] : "pic1.png";

    Mat img = imread(filename, 0);
    if(img.empty())
    {
        cout << "can not open " << filename << endl;
        return -1;
    }

	cv::threshold(img, img, 127, 255, cv::THRESH_BINARY); 
	cv::Mat skel(img.size(), CV_8UC1, cv::Scalar(0));
	cv::Mat temp;
	cv::Mat eroded;
 
	cv::Mat element = cv::getStructuringElement(cv::MORPH_CROSS, cv::Size(2, 2));
	namedWindow( "Display window", WINDOW_AUTOSIZE );
    imshow( "Display window", img );
	bool done;
    
	do
	{
	  cv::erode(img, eroded, element);
	  cv::dilate(eroded, temp, element);
	  cv::subtract(img, temp, temp);
	  cv::bitwise_or(skel, temp, skel);
	  eroded.copyTo(img);
	  done = (cv::countNonZero(img) == 0);
	  //TODO: Generate a rectangle to use to check if the forward path is straight ahead, or if we're angled, based on what point of intersection we see in our rectangle (if none, it's straight)
	  imshow( "Display window", img );
	  waitKey(0);
	} while (!done);
}