# Compiler flags
CFLAGS=-std=c99
CFLAGS+=-g -ggdb3
#CFLAGS+= -O5
CFLAGS+= -O0
LDFLAGS=-lm
PYTHON=python			# Name of Python executable

# Target for building all components
all: gauss_solve libgauss.so

# Object files needed
OBJS = gauss_solve.o main.o helpers.o
gauss_solve.o : gauss_solve.h
helpers.o: helpers.h

# Build the main executable
gauss_solve : $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $@ $(LDFLAGS)

# Check targets (if required by the autograder)
check: check_gauss_solve check_ctype_wrapper

check_gauss_solve: gauss_solve
	./$<

check_ctype_wrapper: gauss_solve.py libgauss.so
	$(PYTHON) ./$<

# Build the shared library for Python 3.10
LIB_SOURCES = gauss_solve.c
libgauss.so: gauss_solve.c
	gcc -shared -I/usr/include/python3.10 -fPIC -o libgauss.so gauss_solve.c

# Clean up build files
clean: FORCE
	@-rm -f gauss_solve *.o *.so main

FORCE:

# Build the main executable and ensure the library is created
main: main.o gauss_solve.o helpers.o
	gcc -o main main.o gauss_solve.o helpers.o -L. -lgauss -lm

main.o: main.c gauss_solve.h
	gcc -c main.c

gauss_solve.o: gauss_solve.c gauss_solve.h
	gcc -c gauss_solve.c
