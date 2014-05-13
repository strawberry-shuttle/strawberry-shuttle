//#include <opencv2/highgui/highgui.hpp>
#include "highgui.h"
int main( int argc, char** argv)
{
	//allocates memory to image data structure IplImage and loads image from command
	//line into it
	IplImage* img = cvLoadImage( argv[1] );

	//creates window
	cvNamedWindow( "Example1", CV_WINDOW_AUTOSIZE );

	
	//shows image in this window
	cvShowImage( "Example!", img);

	//waits 10000 ms or until key is pressed
	cvWaitKey(10000);

	//releases memory that has image
	cvReleaseImage( &img);

	//closes window
	cvDestroyWindow("Example1");
}