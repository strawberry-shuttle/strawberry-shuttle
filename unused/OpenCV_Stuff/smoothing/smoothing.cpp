#include "cv.h"
#include "highgui.h"

int main( int argc, char** argv)
{
	IplImage* pic = cvLoadImage( argv[1] );
	cvNamedWindow("Example4-in");
	cvNamedWindow("Example4-out");
	cvShowImage("Example4-in", pic);
	IplImage* out = cvCreateImage(cvGetSize(pic), IPL_DEPTH_8U, 3 );

	//smoothing
	//can do pic,pic ie save the output over the input if you want
	//cvSmooth( pic, out, CV_GAUSSIAN, 3);
	cvThreshold(pic, out, 90, 90, CV_THRESH_TRUNC);

	cvShowImage("Example4-out", out);

	cvReleaseImage(&out);
	cvWaitKey(0);
	cvDestroyWindow("Example4-in");
	cvDestroyWindow("Example4-out");



}