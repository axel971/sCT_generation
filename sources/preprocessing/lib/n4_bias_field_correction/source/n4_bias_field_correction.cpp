#include <iostream>
#include "itkImageFileReader.h"
#include "itkImageFileWriter.h"
#include "itkN4BiasFieldCorrectionImageFilter.h"

using namespace std;
using namespace itk;

int main(int argc, char* argv[])
{
 using pixelType = float;
 
using imageType = Image<pixelType, 3>;

// declare reader and writer types for the input and output images
using readerType = ImageFileReader<imageType>;
using writerType = ImageFileWriter<imageType>;

// Read the input image
readerType::Pointer readerInputImg = readerType::New();
readerInputImg->SetFileName(argv[1]);
readerInputImg->Update();

// Read the mask
readerType::Pointer readerMask = readerType::New();
readerMask->SetFileName(argv[2]);
readerMask->Update();

// Declare the N4 Itk filter 
using N4Type = N4BiasFieldCorrectionImageFilter<imageType, imageType, imageType>;
N4Type::Pointer N4 = N4Type::New();

// Initialize the filter
N4->SetInput(readerInputImg->GetOutput());
using maximumNumberOfIterationsType = Array<unsigned int> ;
maximumNumberOfIterationsType maximumNumberOfIterations;
maximumNumberOfIterations.SetSize(2);
maximumNumberOfIterations.Fill(4);
N4->SetMaximumNumberOfIterations(maximumNumberOfIterations);
N4->SetNumberOfFittingLevels(2);
N4->SetNumberOfControlPoints(4);
N4->Update();

// Write on the hard disk the output image
writerType::Pointer writer = writerType::New();
writer->SetFileName(argv[3]);
writer->SetInput(N4->GetOutput());
writer->Update();

return 1;
}