// any read access to ledMapping[] and Serial breaks the code (won't run at all), probably too much dynamic memory alloc
// Fuck this shit

#include <Arduino.h>

#include <FastLED.h>
#include "FastLED_RGBW.h"

// //GRBW
// //RGB
// // 24 außen
// // 23 innen
// // unten innen eingespeißt, gegen den Uhrzeigersinn

#define BUTTON_PIN      2
#define DEBOUNCE        200
#define INTERRUPT_MODE  RISING

#define NUM_LEDS    282
#define DATA_PIN    11

CRGBW leds[NUM_LEDS];
CRGB *ledsRGB = (CRGB *) &leds[0];

#define IDLE_ANIM_STEPTIME  20
#define FLASH_TIME          100
#define BRIGHTNESS_IDLE     32
#define BRIGHTNESS_CIRCLE   64

CRGBW black(0, 0, 0, 0);
CRGBW red(255, 0, 0, 0);
CRGBW green(0, 255, 0, 0);
CRGBW blue(0, 0, 255, 0);
CRGBW yellow(255, 255, 0, 0);
CRGBW cyan(0, 255, 255, 0);
CRGBW violet(255, 0, 255, 0);
CRGBW white(0, 0, 0, 255);
CRGBW fullWhite(255, 255, 255, 255);

CRGBW loadingColors[] = {red, yellow, green, cyan, blue, white};


#define STRIP_OUTER_LEN 24
#define STRIP_INNER_LEN 23
/* 
uint16_t ledMapping[NUM_LEDS];

void generateLedMapping() {

    //yes I know, I could've put it in loops too, but that would've been too unreadable imho
    for(uint8_t i = 0; i < STRIP_INNER_LEN; i++) {
        ledMapping[(i + (STRIP_INNER_LEN * 0)) * 2 + 1] = (STRIP_INNER_LEN * 3) - 1 - i;
        ledMapping[(i + (STRIP_INNER_LEN * 1)) * 2 + 2] = (STRIP_INNER_LEN * 2) - 1 - i;
        ledMapping[(i + (STRIP_INNER_LEN * 2)) * 2 + 3] = (STRIP_INNER_LEN * 1) - 1 - i;
        ledMapping[(i + (STRIP_INNER_LEN * 3)) * 2 + 4] = (STRIP_INNER_LEN * 6) - 1 - i;
        ledMapping[(i + (STRIP_INNER_LEN * 4)) * 2 + 5] = (STRIP_INNER_LEN * 5) - 1 - i;
        ledMapping[(i + (STRIP_INNER_LEN * 5)) * 2 + 6] = (STRIP_INNER_LEN * 4) - 1 - i;
    }

    for(uint8_t i = 0; i < STRIP_OUTER_LEN; i++) {
        ledMapping[(i + (STRIP_OUTER_LEN * 0)) * 2 - 0] = (STRIP_OUTER_LEN * 3) - 1 - i + STRIP_INNER_LEN * 6;
        ledMapping[(i + (STRIP_OUTER_LEN * 1)) * 2 - 1] = (STRIP_OUTER_LEN * 2) - 1 - i + STRIP_INNER_LEN * 6;
        ledMapping[(i + (STRIP_OUTER_LEN * 2)) * 2 - 2] = (STRIP_OUTER_LEN * 1) - 1 - i + STRIP_INNER_LEN * 6;
        ledMapping[(i + (STRIP_OUTER_LEN * 3)) * 2 - 3] = (STRIP_OUTER_LEN * 6) - 1 - i + STRIP_INNER_LEN * 6;
        ledMapping[(i + (STRIP_OUTER_LEN * 4)) * 2 - 4] = (STRIP_OUTER_LEN * 5) - 1 - i + STRIP_INNER_LEN * 6;
        ledMapping[(i + (STRIP_OUTER_LEN * 5)) * 2 - 5] = (STRIP_OUTER_LEN * 4) - 1 - i + STRIP_INNER_LEN * 6;
    }
}*/

uint8_t segmentOrder[] = {3, 2, 1, 6, 5, 4};


// magic - do not touch
// should generate the same pattern as generateLedMapping
uint16_t mappedLedNum(uint16_t ledNum) {
    // ledNum *= 2;
    for(uint8_t i = 0; i < 6; i++) {
        //0   1  47   0  48
        //1  48  94  47  95
        //2  95 141  94 142
        //3 142 188 141 189
        //4 189 235 188 236
        //5 236 282 235 283
        uint16_t innerMin = (STRIP_INNER_LEN * i) * 2 + (i + 1);
        uint16_t innerMax = innerMin + STRIP_INNER_LEN * 2;
        uint16_t outerMin = (STRIP_OUTER_LEN * i) * 2 - i;
        uint16_t outerMax = outerMin + STRIP_OUTER_LEN * 2;

        if(ledNum >= innerMin && ledNum < innerMax && ledNum % 2 != i % 2) {
            return (STRIP_INNER_LEN * segmentOrder[i]) - 1 - (ledNum - innerMin) / 2;
        }
        else if(ledNum >= outerMin && ledNum < outerMax && ledNum % 2 == i % 2) {
            return (STRIP_OUTER_LEN * segmentOrder[i]) - 1 - (ledNum - outerMin) / 2 + STRIP_INNER_LEN * 6;
        }
    }
}

uint8_t segmentMapping[] = {2, 1, 0, 5, 4, 3};

void setSegment(uint8_t segment, CRGBW color) {
    segment = segmentMapping[segment];
    uint16_t segmentInnerStart  = segment * 23;
    uint16_t segmentInnerEnd    = segmentInnerStart + 22;
    uint16_t segmentOuterStart  = (23*6) + segment * 24;
    uint16_t segmentOuterEnd    = segmentOuterStart + 23;

    for(uint16_t i = segmentInnerStart; i <= segmentInnerEnd; i++) {
        leds[i] = color;
    }

    for(uint16_t i = segmentOuterStart; i <= segmentOuterEnd; i++) {
        leds[i] = color;
    }

    FastLED.show();

}


void setLed(uint16_t ledNum, CRGBW color) {
    // strip.SetPixelColor(ledMapping[ledNum], color);
    // leds[ledMapping[ledNum]] = color;
    leds[mappedLedNum(ledNum)] = color;
}


void fillColor(CRGBW color) {
    for(uint16_t i = 0; i < NUM_LEDS; i++) {
        leds[i] = color;
    }
}


void testFlash() {
    for(uint8_t i = 0; i < 6; i++) {
        setSegment(i, loadingColors[i]);
        delay(1000);
    }

    fillColor(fullWhite);
    FastLED.show();
    delay(100);
    fillColor(black);
    FastLED.show();
    delay(2000);
}

uint32_t startCircleTime = 0, circleTime = 0;
uint16_t lastUpdatedPixel = 0;
bool circleDone = false;

void stopRainbowCircle() {
    circleTime = 0;
    lastUpdatedPixel = 0;
    circleDone = true;
}

void rainbowCircleLoop() {
    if(circleTime != 0) {
        
        uint16_t currentPixel = ((float)(millis() - startCircleTime) / (float)circleTime) * (float)NUM_LEDS;
        if(currentPixel >= NUM_LEDS) {
            currentPixel = NUM_LEDS - 1;
        }

        for(uint16_t i = lastUpdatedPixel; i <= currentPixel; i++) {
            uint8_t hue = (1 - (float) i / (float)(NUM_LEDS - 1)) * 255;
            setLed(i, (CRGB)CHSV(hue, 255, BRIGHTNESS_CIRCLE));
        }
        FastLED.show();
        lastUpdatedPixel = currentPixel;

        if(currentPixel == NUM_LEDS - 1) {
            stopRainbowCircle();
        }
    }
}


void rainbowCircle(uint32_t time) {
    circleTime = time;
    lastUpdatedPixel = 0;
    circleDone = false;
    fillColor(black);
    startCircleTime = millis();

    // while(circleTime != 0) {
    //     rainbowCircleLoop();
    // }

}

void flash() {
    fillColor(fullWhite);
    FastLED.show();
    delay(FLASH_TIME);
    fillColor(black);
    FastLED.show();
    stopRainbowCircle();
}

void fillPalette(CRGBPalette16 palette, uint8_t index, uint8_t brightness, uint16_t start = 0, uint16_t end = NUM_LEDS) {
    if(end > NUM_LEDS)
        end = end % NUM_LEDS;

    for(uint16_t i = start; i < end; i++) {
        setLed(i, ColorFromPalette(palette, (index + i) % 256, brightness));
    }

    if(end < start) { // wrap around
        for(uint16_t i = start; i < NUM_LEDS; i++) {
            setLed(i, ColorFromPalette(palette, (index + i) % 256, brightness));
        }
        for(uint16_t i = 0; i < end; i++) {
            setLed(i, ColorFromPalette(palette, (index + i + (NUM_LEDS - end)) % 256, brightness));
        }
    }
}

volatile unsigned long lastButtonPress = 0;
bool startCircleAnimation = false, startFlash = false;

void buttonIsr() {
    if(millis() - lastButtonPress > DEBOUNCE && !startCircleAnimation && !startFlash) {
        lastButtonPress = millis();
        startCircleAnimation = true;
        startFlash = true;
    }
}

void setup() {
    Serial.begin(115200);
    Serial.println("Fotobox LED Control");

    pinMode(BUTTON_PIN, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonIsr, INTERRUPT_MODE);

    FastLED.addLeds<WS2812B, DATA_PIN, RGB>(ledsRGB, getRGBWsize(NUM_LEDS));
    FastLED.show();
    // generateLedMapping();

    // Serial.println(ledMapping[0]);
}

bool idleAnimation = true;
unsigned long lastAnimStep = 0;
uint16_t animStep = 0;

void loop() {  

    if(startCircleAnimation) {
            rainbowCircle(6000);
            startCircleAnimation = false;
        }
    if(startFlash && circleTime == 0 && !startCircleAnimation) {
        startFlash = false;
        Serial.print('t');
        flash();
    }
    

    if(Serial.available()) {
        char c = Serial.read();
        switch (c) {
            case 't':
            case 'T':
                idleAnimation = false;
                rainbowCircle(6000);
                break;
            case 'f':
            case 'F':
                flash();
                idleAnimation = true;
                break;
        }
    }

    rainbowCircleLoop();

    if(circleTime == 0 && idleAnimation && millis() - lastAnimStep >= IDLE_ANIM_STEPTIME) {
        lastAnimStep = millis();
        // uint16_t step = (millis() / 10) % NUM_LEDS;

        fillColor(black);

        for(uint8_t i = 0; i < 6; i++) {
            uint16_t offset = animStep % 47;
            uint16_t begin = i * 47 + offset;
            uint16_t end = i * 47 + 16 + offset;
            fillPalette(RainbowColors_p, (animStep * 2) % 256, BRIGHTNESS_IDLE, begin, end);
        }
        FastLED.show();

        animStep++;

    }
}