#Strawberry Shuttle Code

##Processing
Processing is a tool to graphically display stuff. It can connect with the Arduino to dislay real time data sent over the serial port. I used Processing to graph the distance given by both of the ultrasonic sensors. With it I think we can more easily tell when/where the signal is not stable and see the range that the ultrasonic sensor has.

###Instructions for Using Processing to display the serial output from the Arduino
1. Download and install both the [Arduino IDE](http://arduino.cc/en/Main/Software) and [Processing](http://www.processing.org/download/?processing)
2. Download the library for Processing v2.0 from [this](http://playground.arduino.cc/Interfacing/Processing) page
3. That same page has instructions of how to configure it but basically copy the `arduino` folder from the library zip into the `libraries` sub-folder of your Processing Sketchbook. (You can find the location of your Sketchbook by opening the Processing Preferences. If you haven't made a "libraries" sub-folder, create one.) I had to restart Processing after copying it.
4. When you run the code in processing `ping_test\two_ultrasonic_sensors_graphing\two_ultrasonic_sensors_graphing.pde` it displayes the serial interfaces in a list and you may have to modify the array index on line 27 (`myPort = new Serial(this, Serial.list()[1], 9600);`) to choose the right one.
5. Run `ping_test\ping_test.ino` on the Arduino, don't connect with the Serial Monitor, and then run the Processing code and you should see a realtime graph. The red one is sensor 1 and the blue is sensor 2.
