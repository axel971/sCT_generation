# Examples for compiling codes in Windows machines: with cmake, gcc, g++,
mingw.

cmake . -G "MinGW Makefiles" -D CMAKE_C_COMPILER=gcc -D CMAKE_CXX_COMPILER=g++ -Bbuild -DITK_DIR="C:\itk\bin\CMakeFiles"
mingw32-make

