#include "highgui.h"
#include <iostream>
using namespace std;

//call: birdseye board_w board_h boardimage
//uses perspective view of chessboard along with real height and 
//width of board to create homography matrix
int main(int argc, char* argv[])
{
	if(argc != 4)
		return -1;

	int boardWidth = atoi(argv[1]);
	int boardHeight = atoi(argv[2]);
	int boardArea = boardWidth * boardHeight;
	CvSize boardSize = CvSize(boardWidth, boardHeight);
	IplImage* image = 0;
	IplImage* grayImage = 0;


	if( (image = cvLoadImage(argv[3])) == 0)
	{
		cout<<"Could not load image "<<argv[3]<<endl;
		return -1
	}
	int imageWidth = image->width;
	int imageHeight = image->height;
		
	grayImage = cvCreateImage(cvGetSize(image), 8, 1);
	cvCvtColor(image, grayImage, CV_BGR2GRAY);

	//calibration code here...?

	cvNamedWindow("Chessboard");
	CVPoint2D32f* corners = new CVPoint2D32f[boardArea];
	int cornerCount = 0;
	int found = cvFindChessboardCorners(
		image,
		boardSize,
		corners,
		&cornerCount,
		CV_CALIB_CB_ADAPTIVE_THRESH | CV_CALIB_CB_FILTER_QUADS
		);

	if(!found)
	{
		cout<<"Couldn't get chessboard on "<<argv[3]<<" only found "<<cornerCount<<" of "<<
	}

}//main