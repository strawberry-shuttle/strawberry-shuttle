NAME	:= canny_corner
SOURCE	:= $(NAME).cpp
FLAGS	:= `pkg-config --cflags --libs opencv` -O3
OUT	:= $(NAME).out
GCC	:= g++

all:
	$(GCC) $(SOURCE) -o $(OUT) $(FLAGS)

clean:
	rm -rf $(OUT)
