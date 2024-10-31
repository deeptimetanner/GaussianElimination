# Compiler and flags
CC = gcc
CFLAGS = -std=c99 -g -ggdb3
LDFLAGS = -lm

# Target executable
TARGET = gauss_solve

# Object files
OBJS = gauss_solve.o main.o helpers.o

# All target
all: $(TARGET) libgauss.so

# Linking the target executable
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(TARGET) $(LDFLAGS)

# Compile main.o, with gauss_solve.h and helpers.h as dependencies
main.o: main.c gauss_solve.h helpers.h
	$(CC) $(CFLAGS) -c main.c

# Compile gauss_solve.o, with gauss_solve.h as dependency
gauss_solve.o: gauss_solve.c gauss_solve.h
	$(CC) $(CFLAGS) -c gauss_solve.c

# Create shared library for the C implementation
libgauss.so: gauss_solve.c
	$(CC) -shared -fPIC -o libgauss.so gauss_solve.c -lm

# Compile helpers.o, with helpers.h as dependency
helpers.o: helpers.c helpers.h
	$(CC) $(CFLAGS) -c helpers.c

# Clean up build files
clean:
	rm -f *.o $(TARGET) libgauss.so
