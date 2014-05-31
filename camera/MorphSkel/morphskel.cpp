//Based on: http://felix.abecassis.me/2011/09/opencv-morphological-skeleton/

#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

#include <iostream>


//#define LINE_DIST 10 //Line distance from center of image
#define LINE_HEIGHT 175
#define LINE_OFFSET -5
#define FILTER_COUNT 5

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

	threshold(img, img, 127, 255, THRESH_BINARY);
	Mat temp;
	Mat eroded;

	Mat element = getStructuringElement(MORPH_CROSS, Size(2, 2));
	namedWindow( "Display window", WINDOW_AUTOSIZE );
    imshow( "Display window", img );

    waitKey(0);
    //Dilate and Erode image
    for(int i = 0; i < FILTER_COUNT; i++)
    {
	  erode(img, eroded, element);
	  dilate(eroded, temp, element);
	  subtract(img, temp, temp);
	  eroded.copyTo(img);
	  imshow( "Display window", img );
    }
    waitKey(0);

    cout << "Broken out!" << endl;

    //Run Canny to generate edges of the dilated/eroded image
    Mat dst;
    Canny(img, dst, 50, 200, 3);

    imshow( "Display window", dst );

    waitKey(0);

    //Check if there exists any points intercepting the 'invisible' lines
    Size s = dst.size();

    line(dst,Point((s.width/2)+/*LINE_DIST+*/LINE_OFFSET,s.height),Point((s.width/2)+/*LINE_DIST+*/LINE_OFFSET,s.height-LINE_HEIGHT),Scalar(255,0,255),3,CV_AA);
    //line(dst,Point((s.width/2)-LINE_DIST+LINE_OFFSET,s.height),Point((s.width/2)-LINE_DIST+LINE_OFFSET,s.height-LINE_HEIGHT),Scalar(255,0,255),3,CV_AA);
    cout << s.width << "x" << s.height << endl;
    imshow( "Display window", dst);
    waitKey(0);

    return 0;
}
