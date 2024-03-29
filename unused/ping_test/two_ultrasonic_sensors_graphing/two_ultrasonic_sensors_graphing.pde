// Graphing sketch

 
// This program takes ASCII-encoded strings
// from the serial port at 9600 baud and graphs them. It expects values in the
// range 0 to 1023, followed by a newline, or newline and carriage return

// Created 20 Apr 2005
// Updated 18 Jan 2008
// by Tom Igoe
// This example code is in the public domain.

import processing.serial.*;

Serial myPort;        // The serial port
int xPos = 1;         // horizontal position of the graph

void setup () {
  // set the window size:
  size(1024, 768);        
  
  // List all the available serial ports
  println(Serial.list());
  // I know that the first port in the serial list on my mac
  // is always my  Arduino, so I open Serial.list()[0].
  // Open whatever port is the one you're using.
  myPort = new Serial(this, Serial.list()[1], 9600);
  // don't generate a serialEvent() unless you get a newline character:
  myPort.bufferUntil('\n');
  // set inital background:
  background(0);
}
void draw () {
  // everything happens in the serialEvent()
}
 
void serialEvent (Serial myPort) {
  // get the ASCII string:
  String inString1 = myPort.readStringUntil('\t');
  String inString2 = myPort.readStringUntil('\n');
  if (inString1 != null && inString1 != null) {
    // trim off any whitespace:
    inString1 = trim(inString1);
    inString2 = trim(inString2);
    // convert to an int and map to the screen height:
    float inByte1 = float(inString1); 
    float inByte2 = float(inString2); 
    inByte1 = map(inByte1, 0, 200, 0, height);
    inByte2 = map(inByte2, 0, 200, 0, height);
    
    // draw the line:
    stroke(235,0,100,100);
    line(xPos, height, xPos, height - inByte1);
    stroke(13,184,255,100);
    line(xPos, height, xPos, height - inByte2);
    
    // at the edge of the screen, go back to the beginning:
    if (xPos >= width) {
      xPos = 0;
      background(0); 
    } 
    else {
      // increment the horizontal position:
      xPos++;
    }
  }
}
