//Based on: http://felix.abecassis.me/2011/09/opencv-morphological-skeleton/

#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

#include <iostream>


#define LINE_DIST 10 //Line distance from center of image
#define LINE_HEIGHT 175
#define LINE_OFFSET -15


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


    //Dilate and Erode image
	do
	{
	  cv::erode(img, eroded, element);
	  cv::dilate(eroded, temp, element);
	  cv::subtract(img, temp, temp);
	  cv::bitwise_or(skel, temp, skel);
	  eroded.copyTo(img);
	  done = (cv::countNonZero(img) == 0);
	  imshow( "Display window", img );
	  int key = cvWaitKey();
      if(key == 27)
        break;
	} while (!done);

    cout << "Broken out!" << endl;

    //Run Canny to generate edges of the dilated/eroded image
    Mat dst;
    Canny(img, dst, 50, 200, 3);

    imshow( "Display window", dst );

    waitKey(0);

    //Check if there exists any points intercepting the 'invisible' lines
    cv::Size s = dst.size();

    line(dst,Point((s.width/2)+LINE_DIST+LINE_OFFSET,s.height),Point((s.width/2)+LINE_DIST+LINE_OFFSET,s.height-LINE_HEIGHT),Scalar(255,0,255),3,CV_AA);
    line(dst,Point((s.width/2)-LINE_DIST+LINE_OFFSET,s.height),Point((s.width/2)-LINE_DIST+LINE_OFFSET,s.height-LINE_HEIGHT),Scalar(255,0,255),3,CV_AA);
    cout << s.width << "x" << s.height << endl;
    imshow( "Display window", dst);
    waitKey(0);


    return 0;

}
