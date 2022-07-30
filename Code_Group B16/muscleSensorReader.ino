#include "arduinoFFT.h"

#define SAMPLES 128

unsigned int sampling_period_us;
unsigned long microseconds;

double vReal[SAMPLES];
double vImag[SAMPLES];
double average = 0;
int countLoop = 0;

arduinoFFT FFT = arduinoFFT();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  sampling_period_us = round(1000000*(1.0/1000));
}

void loop() {
  countLoop += 1;
  for(int i = 0; i < SAMPLES; i++) {
    microseconds = micros();
    vReal[i] = analogRead(1);
    vImag[i] = 0;
    while(micros() < (microseconds + sampling_period_us)) {}
  }

  FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
  FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);

  double mnf = 0;
  double sumPower = 0;
  for(int i = 0; i < SAMPLES/2; i++) {
    mnf += i * 1.0 * 1000 / SAMPLES * vReal[i];  // add all amplitudes of various frequencies together
    sumPower += vReal[i]; // add all frequencies together
  }
  mnf = mnf / sumPower; // calculate mean frequency

  // take average for denoising purpose
  if(countLoop != 4) average += mnf; 
  else {
    average /= 4;
    Serial.println(average);
    countLoop = 0;
  }
}
