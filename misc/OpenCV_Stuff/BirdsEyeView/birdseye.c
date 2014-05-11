#include <highgui.h>
#include <cv.h>
#include <cxcore.h>
#include <math.h>
#include <vector>
#include <stdio.h>

#include <iostream>

using namespace cv;

using namespace std;

//call: birdseye boardWidth boardHeight boardimage
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
		return -1;
	}
	int imageWidth = image->width;
	int imageHeight = image->height;
		
	grayImage = cvCreateImage(cvGetSize(image), 8, 1);
	cvCvtColor(image, grayImage, CV_BGR2GRAY);

	//calibration code here...?

	cvNamedWindow("Chessboard");
	CvPoint2D32f* corners = new CvPoint2D32f[boardArea];
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
		cout<<"Couldn't get chessboard on "<<argv[3]<<" only found "<<cornerCount<<" of "<<boardArea<<endl;
	}
	return -1;

	//get subpixel accuracy
	cvFindCornerSubPix(
		grayImage,
		corners,
		cornerCount,
		CvSize(11,11),
		cvSize(-1,-1),
		cvTermCriteria(CV_TERMCRIT_EPS | CV_TERMCRIT_ITER, 30, 0.1)
		);

	//GET THE IMAGE AND OBJECT POINTS:
    // We will choose chessboard object points as (r,c):
    // (0,0), (boardWidth-1,0), (0,boardHeight-1), (boardWidth-1,boardHeight-1).
    //

    CvPoint2D32f objPts[4], imgPts[4];
    imgPts[0] = corners[0];
    imgPts[1] = corners[boardWidth-1];
    imgPts[2] = corners[(boardHeight-1)*boardWidth];
    imgPts[3] = corners[(boardHeight-1)*boardWidth + boardWidth-1];

    objPts[0].x = 0; objPts[0].y = 0;
    objPts[1].x = boardWidth -1; objPts[1].y = 0;
    objPts[2].x = 0; objPts[2].y = boardHeight -1;
    objPts[3].x = boardWidth -1; objPts[3].y = boardHeight -1;


    // DRAW THE POINTS in order: B,G,R,YELLOW
    //
    cvCircle( image, cvPointFrom32f(imgPts[0]), 9, CV_RGB(0,0,255), 3); //blue
    cvCircle( image, cvPointFrom32f(imgPts[1]), 9, CV_RGB(0,255,0), 3); //green
    cvCircle( image, cvPointFrom32f(imgPts[2]), 9, CV_RGB(255,0,0), 3); //red
    cvCircle( image, cvPointFrom32f(imgPts[3]), 9, CV_RGB(255,255,0), 3); //yellow
    // DRAW THE FOUND CHESSBOARD
    //

    cvDrawChessboardCorners(
        image,
        boardSize,
        corners,
        cornerCount,
        found
    ); 
    cvShowImage( "Chessboard", image );
    // FIND THE HOMOGRAPHY
    //
    CvMat *H = cvCreateMat( 3, 3, CV_32F);
    cvGetPerspectiveTransform( objPts, imgPts, H);
    Mat homography = H;
    cvSave("Homography.xml",H); //We can reuse H for the same camera mounting

    /**********************GENERATING 3X4 MATRIX***************************/

    // LET THE USER ADJUST THE Z HEIGHT OF THE VIEW
    //
    float Z = 23;
    int key = 0;
    IplImage *birds_image = cvCloneImage(image);
    cvNamedWindow("Birds_Eye");
    // LOOP TO ALLOW USER TO PLAY WITH HEIGHT:
    //
    // escape key stops
    //
    while(key != 27) {
        // Set the height
        //
        CV_MAT_ELEM(*H,float,2,2) = Z;
        // COMPUTE THE FRONTAL PARALLEL OR BIRD’S-EYE VIEW:
        // USING HOMOGRAPHY TO REMAP THE VIEW
        //
    cvWarpPerspective(
    image,
    birds_image,
    H,
    CV_INTER_LINEAR | CV_WARP_INVERSE_MAP | CV_WARP_FILL_OUTLIERS
    );
    cvShowImage( "Birds_Eye", birds_image );
    imwrite("/home/lee/bird.jpg", birds_image);

    key = cvWaitKey();
    if(key == 'u') Z += 0.5;
    if(key == 'd') Z -= 0.5;
    }
    return 0;

}//main