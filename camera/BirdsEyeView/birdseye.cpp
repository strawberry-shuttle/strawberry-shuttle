#include <highgui.h>
#include <cv.h>
#include <cxcore.h>
#include <math.h>
#include <vector>
#include <stdio.h>

#include <iostream>

using namespace cv;

using namespace std;



void setObjPts(CvPoint2D32f objPts[], int boardHeight,int boardWidth)
{
    objPts[0].x = 0; objPts[0].y = 0;
    objPts[1].x = boardWidth ; objPts[1].y = 0;
    objPts[2].x = 0; objPts[2].y = boardHeight;
    objPts[3].x = boardWidth ; objPts[3].y = boardHeight;  
}

void getCorners(IplImage* image, int imageWidth, int imageHeight,CvPoint2D32f dots[])
{
    int key = 0 ;

    //keeping original image
    IplImage *orig = cvCloneImage(image);
    
    cvNamedWindow("Image",CV_WINDOW_AUTOSIZE);
    
    //draw first point
    cvCircle( image, cvPointFrom32f((dots)[0]), 4, CV_RGB(0,0,255), 2); //blue
    cvShowImage( "Image", image );
    int i = 0;


    while(key != 27 || (i < 4 && i >=1))
    {
        //gets user's key pressed
        key = cvWaitKey();

        //moves position of given dot
        if(key == 'a') 
            (dots)[i].x -= 5;
        if(key == 'd') 
            (dots)[i].x += 5;
        if(key == 'w') 
            (dots)[i].y -= 5;
        if(key == 's') 
            (dots)[i].y += 5;

        if(key == 'h') 
            (dots)[i].x -= 2;
        if(key == 'k') 
            (dots)[i].x += 2;
        if(key == 'u') 
            (dots)[i].y -= 2;
        if(key == 'j') 
            (dots)[i].y += 2;

        //'l' means toggle to next dot
        if(key == 'n')
            i++; 
        //toggle to previous point
         if(key == 'p')
            i--; 


        //places new position of all dots
        for(int j = 0; j<4; j++)
            cvCircle( image, cvPointFrom32f((dots)[j]), 4, CV_RGB(0,0,255), 2); //blue
        

        cvShowImage( "Image", image );

        // clears image of dots (otherwise there would be dot at every point in the path of movement)
        image = cvCloneImage(orig);
   }
  
   cvReleaseImage(&orig);
   return;
   
}

CvMat* adjustHeight(IplImage* image, CvMat* H, CvPoint2D32f imgPts[], CvPoint2D32f objPts[],int boardHeight,int boardWidth)
{
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
        setObjPts(objPts,boardHeight,boardWidth);
        cvGetPerspectiveTransform( objPts, imgPts, H);
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
    cvShowImage("Chessboard", image);
    cvShowImage( "Birds_Eye", birds_image );

    key = cvWaitKey();
    if(key == 'u') Z += 0.5;
    if(key == 'j') Z -= 0.5;
    if(key == 'w') boardHeight += 1;
    if(key == 's') boardHeight -=1;
    if(key == 'a') boardWidth -=1;
    if(key == 'd') boardWidth +=1;
    }//while
    cvSave("H.xml",H);
    return H;
    
}

CvMat* getHMatrix(IplImage* image, int boardWidth, int boardHeight)
{
    IplImage* test = cvCloneImage(image);
    IplImage* grayImage = 0;
    int cornerCount = 4;
    int boardArea = boardWidth * boardHeight;
    CvSize boardSize = cvSize(boardWidth, boardHeight);
    int imageWidth = image ->width;
    int imageHeight = image->height;
    grayImage = cvCreateImage(cvGetSize(image), 8, 1);
    cvCvtColor(image, grayImage, CV_BGR2GRAY);

    //calibration code here... possibly

    cvNamedWindow("Chessboard");
    CvPoint2D32f dot = cvPoint2D32f(imageWidth / 2.0,imageHeight / 2.0);
    CvPoint2D32f corners[4] = {dot, dot, dot, dot};
    getCorners(test,imageWidth,imageHeight,corners);
    

    CvPoint2D32f objPts[4], imgPts[4]; 
    for(int i =0; i<4; i++)
        imgPts[i] = corners[i];

    setObjPts(objPts,boardHeight,boardWidth);

    
    
    
  
    cvShowImage( "Chessboard", image );
    
    // FIND THE HOMOGRAPHY
    CvMat *H = cvCreateMat( 3, 3, CV_32F);
    cvGetPerspectiveTransform( objPts, imgPts, H);
    Mat homography = H;
    cvSave("Homography.xml",H); //We can reuse H for the same camera mounting  
    H = adjustHeight(image, H, imgPts,objPts,boardHeight,boardWidth);
    return H;
}
    

//call: birdseye boardWidth boardHeight boardimage
//uses perspective view of chessboard along with real height and 
//width of board to create homography matrix
int main(int argc, char* argv[])
{
	IplImage* image = 0;

    CvCapture* capture;
    if(argc <= 3)
        capture = cvCreateCameraCapture(0);
    else
    {
    
      capture = cvCreateFileCapture(argv[3]);  
    }
        
    assert(capture != NULL);
	image = cvQueryFrame( capture );


    // int key = 0;
    // while(key != 27)
    // {

        
    //     cvNamedWindow("evan");
    //     cvShowImage( "evan", image );
    //     key = cvWaitKey();
    // }
   


 
    int boardWidth = atoi(argv[1]);
    int boardHeight = atoi(argv[2]);

    CvMat* H = getHMatrix(image, boardWidth, boardHeight);
 //    // for(int i =0; i < H)
    return 0;

}//main