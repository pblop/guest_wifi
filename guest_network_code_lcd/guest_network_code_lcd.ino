// include the library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// make some custom characters:
byte full[8] = {
  0b11111,
  0b11111,
  0b11111,
  0b11111,
  0b11111,
  0b11111,
  0b11111,
  0b11111
};

void setup() {
  // initialize LCD and set up the number of columns and rows:
  lcd.begin(16, 2);
  Serial.begin(9600);

  // create a new character
  lcd.createChar(0, full);
  Serial.write("online");
}

void fill_row(int row, int number) {
  for (int i = 0; i < number; i++) {
    lcd.setCursor(i, row);
    lcd.write(byte(0));
  }
}

void execute_command(String name, String value) {
//  Serial.println(name + ": " + value);
  if (name == "code") {
    // Write the code
    lcd.setCursor(0, 0);
    lcd.write("                "); // clear bar
    lcd.setCursor(0, 0);
    lcd.print(value);
  } else if (name == "seconds") {
    // Write the remaining seconds bar
    lcd.setCursor(0, 1);
    lcd.write("                "); // clear bar
    lcd.setCursor(0, 1);
    fill_row(1, value.toInt());
  }
}

void loop() {
  String name = "";
  String value = "";
  bool writeToName = true;
  // Parse commands
  while (Serial.available() > 0) {
    delay(2);
    char ch = Serial.read();
    
    if (ch == ';') {
      // Execute the command
      execute_command(name, value);

      // Reset variables
      name = "";
      value = "";
      writeToName = true;
    } else if (ch == '=') {
      writeToName = false;
    } else {
      if (writeToName) {
        name += ch;
      } else {
        value += ch;
      }
    }
    
  }
}
