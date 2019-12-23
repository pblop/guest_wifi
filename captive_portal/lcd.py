from RPLCD import CharLCD
import RPi.GPIO as GPIO

full_square = (0b11111, ) * 8

class LCD:
  def __init__(self):
    GPIO.setwarnings(False)
    self.lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2, pin_rs=40, pin_e=38, pins_data=[36, 37, 35, 33])
    self.lcd.cursor_mode = 'hide'
    self.lcd.create_char(0, full_square)

  def write(self, code, seconds_remaining):
    '''
    Keyword arguments:
    code -- the code to be displayed
    seconds_remaining -- the seconds remaining (max 16)
    '''
    self.clear()

    # Center code horizontally
    LCD_WIDTH = 16
    lcd_y = (LCD_WIDTH - len(str(code))) // 2
    self.lcd.cursor_pos = (0, lcd_y)
  
    self.lcd.write_string(code)
    self.lcd.cursor_pos = (1, 0)
    self.lcd.write_string(chr(0) * seconds_remaining)
  
  def clear(self):
    self.lcd.clear()




