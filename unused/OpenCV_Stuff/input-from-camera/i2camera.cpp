#include "highgui.h"
#include "cv.h"

int main( int argc, char** argv)
{
	cvNamedWindow("Example 2", CV_WINDOW_NORMAL);
	cvNamedWindow("out", CV_WINDOW_NORMAL);
	CvCapture* capture;
	if(argc == 1)
		capture = cvCreateCameraCapture(0);
	else
		capture = cvCreateFileCapture(argv[1]);
	assert(capture != NULL);

	IplImage* frame;
	IplImage* out;
	while(1)
	{
		frame = cvQueryFrame( capture );
		if (!frame)
			break;
		out = frame;
		cvShowImage("Example 2", frame);
		cvThreshold(frame, out, 50, 50, CV_THRESH_TRUNC);
		cvShowImage("out", out);
		char c = cvWaitKey(100);
		if(c == 27)
			break;
	}
	cvReleaseCapture(&capture);
	cvDestroyWindow("Example 2");
}