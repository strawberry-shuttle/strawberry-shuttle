#include <highgui.h>
#include <cv.h>
#include <cxcore.h>
#include <math.h>
#include <vector>
#include <stdio.h>

#include <iostream>

using namespace cv;

using namespace std;
void CallBackFunc(int event, int x, int y, int flags, void* userdata)
{
     if  ( event == EVENT_LBUTTONDOWN )
     {
          cout << "Left button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;
     }
     else if  ( event == EVENT_RBUTTONDOWN )
     {
          cout << "Right button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;
     }
     else if  ( event == EVENT_MBUTTONDOWN )
     {
          cout << "Middle button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;
     }
     else if ( event == EVENT_MOUSEMOVE )
     {
          cout << "Mouse move over the window - position (" << x << ", " << y << ")" << endl;

     }
}
int main(int argc, char* argv[])
{
	int key = 0;
	IplImage* image = 0;
	if( (image = cvLoadImage(argv[1])) == 0)
	{
		cout<<"Could not load image "<<argv[1]<<endl;
		return -1;
	}
	IplImage *temp = cvCloneImage(image);
	int imageWidth = image->width;
	int imageHeight = image->height;
	cout<<"height "<<imageHeight<<" width "<<imageWidth<<endl;

	cvNamedWindow("Image",CV_WINDOW_AUTOSIZE);
	CvPoint2D32f dot = cvPoint2D32f(imageWidth-200.0,imageHeight-200.0);
	CvPoint2D32f dot2 = cvPoint2D32f(imageWidth-200.0,imageHeight-200.0);
	cvCircle( image, cvPointFrom32f(dot), 4, CV_RGB(0,0,255), 2); //blue
	cvCircle( image, cvPointFrom32f(dot2), 4, CV_RGB(0,0,255), 2); //blue
	cvShowImage( "Image", image );
	while(key != 27) 
	{
		
		key = cvWaitKey();
    if(key == 'h') 
    	dot.x -= 2;
    if(key == 'k') 
    	dot.x += 2;
    if(key == 'u') 
    	dot.y -= 2;
    if(key == 'j') 
    	dot.y += 2;

    if(key == 'a') 
    	dot2.x -= 2;
    if(key == 'd') 
    	dot2.x += 2;
    if(key == 'w') 
    	dot2.y -= 2;
    if(key == 's') 
    	dot2.y += 2;


    cvCircle( image, cvPointFrom32f(dot), 4, CV_RGB(0,0,255), 2); //blue
    cvCircle( image, cvPointFrom32f(dot2), 4, CV_RGB(0,255,0), 2); //blue
    cvShowImage( "Image", image );
    image = cvCloneImage(temp);
   }
   cout<<endl<<dot.x<<" "<<dot.y<<endl;
   cout<<endl<<dot2.x<<" "<<dot2.y<<endl;
   cvReleaseImage(&image);
   cvReleaseImage(&temp);
	return 0;
}
