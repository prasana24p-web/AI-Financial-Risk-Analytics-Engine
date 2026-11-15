CC = gcc
CFLAGS = -Wall -Wextra -O2 -Iinclude -fPIC
TARGET = build/libriskengine.so
SRC = src/risk_engine.c

all: $(TARGET)

$(TARGET): $(SRC)
	mkdir -p build
	$(CC) $(CFLAGS) -shared -o $(TARGET) $(SRC)

clean:
	rm -rf build

.PHONY: all clean
