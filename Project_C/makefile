CC=gcc-13
CFLAGS=-Wall -O3 -fopenmp
LDFLAGS=-lm
OBJ=main.o mandelbrot.o pgm.o

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS)

main: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS)

clean:
	rm -f $(OBJ) main

.PHONY: clean

