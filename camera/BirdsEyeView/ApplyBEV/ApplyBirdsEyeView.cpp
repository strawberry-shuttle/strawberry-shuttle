#include <highgui.h>
#include <cv.h>
#include <cxcore.h>
#include <math.h>
#include <vector>
#include <stdio.h>
#include <iostream>
#include <typeinfo>
using namespace cv;
using namespace std;

int main(int argc, char* argv[])
{
	const char *filename = "H.xml";
	if (argc > 1)
		filename = argv[1];
	//Load H matrix
	CvMat* Hpt = (CvMat*)cvLoad(filename);

	Mat H(Hpt);

	namedWindow("vijay",CV_WINDOW_AUTOSIZE);

	//Load image
	Mat image;
	if(argc > 2)
		image = imread(argv[2],CV_LOAD_IMAGE_GRAYSCALE);
	else
		image = imread("pic1.png",CV_LOAD_IMAGE_GRAYSCALE);

	imshow("vijay",image);

	waitKey(0);

	Mat birds_image;
	//Apply H matrix to image
	warpPerspective(
   image,
   birds_image,
   H,
   image.size(),
   INTER_LINEAR | WARP_INVERSE_MAP //| WARP_FILL_OUTLIERS
   );
	
	imshow("vijay",birds_image);
	cvWaitKey(0);

}