//Based on: http://felix.abecassis.me/2011/09/opencv-morphological-skeleton/

#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

#include <iostream>
#include <cmath>


//#define LINE_DIST 10 //Line distance from center of image
#define LINE_HEIGHT 0
#define LINE_OFFSET -40
#define FILTER_COUNT 5
#define MIN_HEIGHT 0 //How far up the line we go
#define POINT_THRESHOLD 5 //How off a point can be from the predicted value when determining line slope

using namespace cv;
using namespace std;

struct line_info
{
    float slope;
    float intercept;
};


float getLineAngle(const vector<line_info> &lines, int x, int y, Mat &dst) //Search around the point of intersection for 2 points to generate a line
{
    cout << "Intersection point found at " << x << "," << y << endl;
    float angle = 0;
    //Go through each line and check what line corresponds to this point, if any
    int i;
    for(i = 0; i < lines.size(); i++)
        if(abs(y - (lines[i].slope) * x + lines[i].intercept) < POINT_THRESHOLD) //Point exists on, or close to, the line
        {
            float m = lines[i].slope;
            float b = lines[i].intercept;
            cout << "Found line for " << x << "," << y << " m = " << m << " b = " << b << endl;
            circle(dst,Point(x,y),20,Scalar(255,0,255),3,CV_AA);
            line(dst,Point(x,y),Point(x+20,(x+20)*m + b),Scalar(255,0,255),3,CV_AA);

            //Get the angle of this line versus a vertical line
            float tmp = x/(m*x+b);
            cout << tmp << endl;
            angle = atan2(x,m*x+b);
            break;
        }
    return angle * 180/CV_PI;

}


int main(int argc, char** argv)
{
    const char* filename = argc >= 2 ? argv[1] : "pic1.png";

    Mat img = imread(filename, 0);
    if(img.empty())
    {
        cout << "can not open " << filename << endl;
        return -1;
    }

	threshold(img, img, 127, 255, THRESH_BINARY); //Apply a binary threshold
	Mat temp;
	Mat eroded;

	Mat element = getStructuringElement(MORPH_CROSS, Size(2, 2));
	namedWindow( "Display window", WINDOW_AUTOSIZE );
    imshow( "Display window", img );

    waitKey(0);
    //Dilate and Erode image
    for(int i = 0; i < FILTER_COUNT; i++)
    {
	  erode(img, eroded, element);
//	  dilate(eroded, temp, element);
//	  subtract(img, temp, temp);
	  eroded.copyTo(img);
	  imshow( "Display window", img );
    }
    waitKey(0);

    cout << "Broken out!" << endl;

    //Run Canny to generate edges of the dilated/eroded image
    Mat dst;
    Canny(img, dst, 50, 200, 3);

    imshow( "Display window", dst );

    waitKey(0);

    //Check if there exists any points intercepting the 'invisible' lines
    Size s = dst.size();


//    if(LINE_HEIGHT)
//        line(dst,Point((s.width/2)+/*LINE_DIST+*/LINE_OFFSET,s.height),Point((s.width/2)+/*LINE_DIST+*/LINE_OFFSET,s.height-LINE_HEIGHT),Scalar(255,0,255),3,CV_AA);
//    else
//        line(dst,Point((s.width/2)+/*LINE_DIST+*/LINE_OFFSET,s.height),Point((s.width/2)+/*LINE_DIST+*/LINE_OFFSET,s.height-s.height),Scalar(255,0,255),3,CV_AA);
    cout << s.width << "x" << s.height << endl;


    //Go up the line and find an intersection point
    float offset = 0;

    //Find every line in the image
    vector<Vec4i> lines;
    vector<line_info> linesinfo;

    HoughLinesP(dst,lines,1,CV_PI/180,10,2,5);

    for(int i = 0; i < lines.size(); i++)
    {
        struct line_info tmp;
        float xdiff = lines[i][2]-lines[i][0];
        if(xdiff) //If it's a vertical line, we don't care
            tmp.slope = (lines[i][3]-lines[i][1])/xdiff;
        else
            tmp.slope = 0.0;
        tmp.intercept = lines[i][1] - lines[i][0]*tmp.slope;

        linesinfo.push_back(tmp);
    }

    int x = s.width/2 + LINE_OFFSET;
    for(int i = s.height; i > MIN_HEIGHT; i--)
    {
        if(dst.at<bool>(x,i))
            if((offset = getLineAngle(linesinfo,x,i,dst)) != 0)
                break;
    }

    imshow( "Display window", dst);
    waitKey(0);
    cout << "Angle: "<< offset << endl;
    return offset; //Return the angle
}
