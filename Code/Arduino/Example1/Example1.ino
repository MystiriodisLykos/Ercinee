int bullet_bill[20][10] = {
  {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
  {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
  {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
  {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
  {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
  {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
  {0, 1, 1, 1, 0, 0, 1, 1, 1, 0},
  {0, 1, 1, 0, 0, 0, 1, 1, 1, 0},
  {1, 1, 1, 0, 0, 1, 1, 1, 1, 1},
  {1, 1, 0, 0, 0, 1, 1, 1, 1, 1},
  {1, 1, 0, 0, 0, 0, 1, 1, 1, 1},
  {1, 1, 1, 0, 0, 1, 1, 1, 1, 1},
  {1, 1, 1, 1, 1, 1, 0, 0, 0, 1},
  {0, 1, 1, 1, 1, 0, 0, 0, 1, 0},
  {0, 1, 1, 1, 1, 0, 1, 1, 1, 0},
  {0, 0, 1, 1, 1, 0, 0, 1, 0, 0},
  {0, 0, 0, 1, 1, 1, 1, 0, 0, 0},
  {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
  {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
  {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
  };


void setup() {
  DDRB |= B00111110; // Setting pins 9-13 to be output. These will be the row pins
  PORTB &= B11000001;  // Setting pins 9-13 low
  DDRD |= B01111100; // Setting pins 2-6 to be output. These will be column pins
  PORTD &= B00000011;  // Setting pins 2-6 low
}

void loop() {
  leds_on(bullet_bill, 2000);  // Display bullet bill for 2000 milliseconds(2 second).
  delay(500);  // Don't do anything for 500 milliseconds(0.5 seconds).
}

void led_on(int row, int col, double delta) {
  row <<= 1;  // Right shift the row by 1 so the least significant bit is a 0.
  col += 8;  // The hardware is set up so that when a col less than 8 is provided no leds turn on.
  col <<= 2;  // Right shift the col by 2 so the 2 least significant bits are 0.
  PORTB |= row;  // Turn the pins associated with the row high.
  PORTD |= col;  // Turn the pins associated with the col high.
  delayMicroseconds(int(delta*1000));
  PORTD &= B00000011;  // Turn the pins associated with the row low.
  PORTB &= B11000001;  // Turn the pins associated with the col low.
}

void leds_on(int leds[20][10], double delta){
  unsigned long start = millis();
  int i = 0, j = 0;
  while(millis()-start < delta) {
    while(millis()-start < delta && j < 10) {
      if(leds[i][j++]) {
        led_on(i, j-1, 0.01);
      }
    }
    i = (i+1)%20;
    j = 0;
  }
}

