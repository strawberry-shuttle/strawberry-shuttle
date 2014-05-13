#include "highgui.h"

int main( int argc, char** argv)
{
	cvNamedWindow("Example 2", CV_WINDOW_AUTOSIZE);
	CvCapture* capture = cvCreateFileCapture( argv[1]);
	IplImage* frame;
	while(1)
	{
		frame = cvQueryFrame( capture );
		if (!frame)
			break;
		cvShowImage("Example 2", frame);
		char c = cvWaitKey(15);
		if(c == 27)
			break;
	}
	cvReleaseCapture(&capture);
	cvDestroyWindow("Example 2");
}