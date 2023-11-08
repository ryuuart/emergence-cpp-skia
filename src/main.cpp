#include <iostream>
#include "SkCanvas.h"
#include "SkColor.h"
#include "SkImage.h"
#include "SkStream.h"
#include "SkRect.h"
#include "SkPaint.h"
#include "SkBitmap.h"
#include "SkEncodedImageFormat.h"
#include "SkPngEncoder.h"

int main() {
    // Define the image dimensions
    int width = 400;
    int height = 300;

    // Create an SkImageInfo for the image (RGBA 8888 format)
    SkImageInfo info = SkImageInfo::MakeN32Premul(width, height);

    // Create a SkBitmap to draw on
    SkBitmap bitmap;
    bitmap.allocPixels(info);

    // Create a canvas to draw on the bitmap
    SkCanvas canvas(bitmap);

    // Clear the canvas with a white background
    canvas.clear(SK_ColorWHITE);

    // Create a red paint
    SkPaint paint;
    paint.setColor(SK_ColorRED);

    // Create a rectangle
    SkRect rect = SkRect::MakeLTRB(50, 50, 350, 250);

    // Draw the red rectangle on the canvas
    canvas.drawRect(rect, paint);

    // Make it green
    paint.setColor(SK_ColorGREEN);
    canvas.drawRect(SkRect::MakeLTRB(10, 10, 100, 150), paint);

    // Encode the bitmap to a PNG image and save it to a file
    SkFILEWStream fileStream("output.png");
    SkPngEncoder::Encode(&fileStream, bitmap.pixmap(), SkPngEncoder::Options());

    // Output success message
    std::cout << "Image saved to output.png" << std::endl;

    return 0;
}
