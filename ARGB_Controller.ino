#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

// Most of this code is taken straight from the Adafruit WS2812b example(s), so go there for how to
// do the stuff :). Just adding in code to allow for changing effects/settings live so it can be
// used as an ARGB controller for computers with out the port on the motherboard

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN            15

#define SERIAL_BUFFER_SIZE 512

// How many NeoPixels are attached to the Arduino?
uint16_t numPixels = 42;

byte serialBuffer[SERIAL_BUFFER_SIZE];

Adafruit_NeoPixel strip = Adafruit_NeoPixel(numPixels, PIN, NEO_GRB + NEO_KHZ800);
 
uint16_t delayVal = 10; // delay used for cycling effects
int brightness = 10; // brightness modifier applied to effects

enum effectList {
  EFFECT_SOLID,
  EFFECT_RAINBOW,
  EFFECT_CHASE,
  EFFECT_WIPE
};

enum settingList {
  SETTING_BRIGHTNESS,
  SETTING_DELAY,
  SETTING_LENGTH
};

int currentEffect = EFFECT_RAINBOW;

uint32_t chaseColor = 0; // Color for the chase effect
uint8_t chaseSize = 1;   // Number of LEDs to light during chase effect
uint16_t chaseStart = 0; // Variable to hold the current start LED of the chase effect

uint32_t solidColor = 0; // Color for the solid effect
uint32_t wipeColor = 0;  // Color for the wipe effect

void setup() 
{
  strip.begin(); // This initializes the NeoPixel library.
  strip.setBrightness(brightness);
  strip.show();
  Serial.begin(115200);
}

// Rainbow cycle along whole strip. Pass delay time (in ms) between frames.
void rainbow() {
  // Hue of first pixel runs 5 complete loops through the color wheel.
  // Color wheel has a range of 65536 but it's OK if we roll over, so
  // just count from 0 to 5*65536. Adding 256 to firstPixelHue each time
  // means we'll make 5*65536/256 = 1280 passes through this outer loop:
  for(long firstPixelHue = 0; firstPixelHue < 5*65536; firstPixelHue += 256) {
    for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
      // Offset pixel hue by an amount to make one full revolution of the
      // color wheel (range of 65536) along the length of the strip
      // (strip.numPixels() steps):
      int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());
      // strip.ColorHSV() can take 1 or 3 arguments: a hue (0 to 65535) or
      // optionally add saturation and value (brightness) (each 0 to 255).
      // Here we're using just the single-argument hue variant. The result
      // is passed through strip.gamma32() to provide 'truer' colors
      // before assigning to each pixel:
      strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
    }
    strip.show(); // Update strip with new contents
    if (Serial.available() > 0){
      return;
    }
    if(Serial.available() > 0) return;
    delay(delayVal);  // Pause for a moment

  }
}

// Fill strip pixels one after another with a color. Strip is NOT cleared
// first; anything there will be covered pixel by pixel. Pass in color
// (as a single 'packed' 32-bit value, which you can get by calling
// strip.Color(red, green, blue) as shown in the loop() function above),
// and a delay time (in milliseconds) between pixels.
void effectWipe(uint32_t color) {
  for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
    strip.setPixelColor(i, color);         //  Set pixel's color (in RAM)
    strip.show();                          //  Update strip to match
    if(Serial.available() > 0) return;
    delay(delayVal);                           //  Pause for a moment
  }
}


// Fill strip with a solid color
void effectSolid(uint32_t color) {
  for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
    strip.setPixelColor(i, color);         //  Set pixel's color (in RAM)
  }
  strip.show();                          //  Update strip to match
}

// Strip will display a block of specified color that will move
// down the strip starting with the first LED and moving to the last,
// wrapping around to the beginning when the end is reached
void ledChase(){
  strip.clear();
  int stripSize = strip.numPixels();
  int ledNum;
  for(int i = 0; i < chaseSize; i++) { // For each pixel in strip...
    if (chaseStart + i >= stripSize){
      ledNum = chaseStart - stripSize + i;
    } else {
      ledNum = chaseStart + i;
    }
    
    strip.setPixelColor(ledNum, chaseColor);         //  Set pixel's color (in RAM)
    if(Serial.available() > 0) return;
  }
  chaseStart++;
  if (chaseStart >= strip.numPixels()){
    chaseStart = 0;
  }
  strip.show();                          //  Update strip to match
}

void parseCommand(byte* commandBytes, int byteSize){
  switch(commandBytes[0]){
    case 'S':
      if(byteSize > 4){
        Serial.println("Bad input command!!!");
        Serial.println((char*)commandBytes);
      }
      switch(commandBytes[1]){
        case SETTING_BRIGHTNESS: // Set brightness
          brightness = commandBytes[2];
          Serial.print("Brightness set to: ");
          Serial.println(brightness);
          break;
        case SETTING_DELAY: // Set effect cycle delay
          delayVal = commandBytes[2];
          if (byteSize > 3){
            delayVal <<= 8;
            delayVal += commandBytes[3];
          }
          Serial.print("Delay set to: ");
          Serial.println(delayVal);
          break;
        case SETTING_LENGTH:
          numPixels = commandBytes[2];
          numPixels <<= 8;
          numPixels += commandBytes[3];
          strip.clear();
          strip.show();
          strip.updateLength(numPixels);
          Serial.print("Number of LEDs set to: ");
          Serial.println(numPixels);
          break;
      }
      break;
    case 'E':
      if(byteSize > 6){
        Serial.println("Bad input command!!!");
        Serial.println((char*)commandBytes);
      }
      switch(commandBytes[1]){
        case EFFECT_SOLID: // Solid color effect
          solidColor = strip.Color(commandBytes[2], commandBytes[3], commandBytes[4]);
          currentEffect = EFFECT_SOLID;
          Serial.println("Effect set to: Solid");
          break;
        case EFFECT_WIPE: // Color wipe effect
          wipeColor = strip.Color(commandBytes[2], commandBytes[3], commandBytes[4]);
          currentEffect = EFFECT_WIPE;
          Serial.println("Effect set to: Wipe");
          break;
        case EFFECT_RAINBOW: // Rainbow effect
          currentEffect = EFFECT_RAINBOW;
          Serial.println("Effect set to: Rainbow");
          break;
        case EFFECT_CHASE: // Chase effect
          chaseStart = 0;
          chaseColor = strip.Color(commandBytes[2], commandBytes[3], commandBytes[4]);
          chaseSize = commandBytes[5];
          Serial.print("Chase Size set to: ");
          Serial.println(chaseSize);
          currentEffect = EFFECT_CHASE;
          Serial.println("Effect set to: Chase");
          break;
      }
    break;
  }
  return;
}

void loop() {
  strip.setBrightness(brightness);
  switch(currentEffect){
    case EFFECT_SOLID:
      effectSolid(solidColor);
      break;
    case EFFECT_RAINBOW:
      rainbow();
      break;
    case EFFECT_CHASE:
      ledChase();
      break;
    case EFFECT_WIPE:
      strip.clear();
      strip.show();
      effectWipe(wipeColor);
  }

  while (Serial.available() > 0){
    int bytesRead = Serial.readBytes(serialBuffer, SERIAL_BUFFER_SIZE);
    parseCommand(serialBuffer, bytesRead);
  }
  delay(delayVal);  // Pause for a moment
}
