#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <stdlib.h>
#include <stdio.h>

using namespace cv;

/// Global variables

Mat src, src_gray;
Mat dst, detected_edges;

int edgeThresh = 1;
int ratio = 3;
int kernel_size = 3;
char* window_name = "Edge Map";

double k = 1.0/100000;

void CannyCorner(int, void*)
{
  /// Reduce noise with a kernel 3x3
  blur( src_gray, detected_edges, Size(3,3) );

  /// Canny detector
  Canny( detected_edges, detected_edges, 147, 147, kernel_size );


  //Use Harris corner detection to pinpoint what we want (the convergence point)
  cornerHarris(detected_edges, dst, 2, 3, k, BORDER_DEFAULT);


//  src.copyTo( dst, detected_edges);
  imshow( window_name, dst );
 }


/** @function main */
int main( int argc, char** argv )
{
  /// Load an image
  src = imread( argv[1] );

  if( !src.data )
  { return -1; }

  /// Create a matrix of the same type and size as src (for dst)
  dst.create( src.size(), src.type() );

  /// Convert the image to grayscale
  cvtColor( src, src_gray, CV_BGR2GRAY );

  /// Create a window
  namedWindow( window_name, CV_WINDOW_AUTOSIZE );

  /// Show the image
  CannyCorner(0, 0);

  /// Wait until user exit program by pressing a key
  waitKey(0);

  return 0;
}
