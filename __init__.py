import RPi.GPIO as GPIO
import time
import smbus
from smbus import SMBus
from time import sleep

ALIGN_FUNC = {
    'left': 'ljust',
    'right': 'rjust',
    'center': 'center'}
CLEAR_DISPLAY = 0x01
ENABLE_BIT = 0b00000100
LINES = {
    1: 0x80,
    2: 0xC0,
    3: 0x94,
    3: 0xD4}

LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

class LCD(object):
    
    def __init__(self, address=0x27, bus=1, width=20, rows=4, backlight=True):
        self.address = address
        self.bus = SMBus(bus)
        self.delay = 0.0005
        self.rows = rows
        self.width = width
        self.backlight_status = backlight
        
        self.write(0x33)
        self.write(0x32)
        self.write(0x06)
        self.write(0x0C)
        self.write(0x28)
        self.write(CLEAR_DISPLAY)
        sleep(self.delay)
        
    def _write_byte(self, byte):
        self.bus.write_byte(self.address, byte)
        self.bus.write_byte(self.address, (byte | ENABLE_BIT))
        sleep(self.delay)
        self.bus.write_byte(self.address, (byte & ~ENABLE_BIT))
        sleep(self.delay)
        
    def write(self, byte, mode=0):
        backlight_mode = LCD_BACKLIGHT if self.backlight_status else LCD_NOBACKLIGHT
        self._write_byte(mode | (byte & 0xF0) | backlight_mode)
        self._write_byte(mode | (byte << 4) & 0xF0 | backlight_mode)
        
    def text(self, text, line, align='left'):
        self.write(LINES.get(line, LINES[1]))
        text, other_lines = self.get_text_line(text)
        text = getattr(text, ALIGN_FUNC.get(align, 'ljust'))(self.width)
        for char in text:
            self.write(ord(char), mode=1)
            if other_lines and line <= self.rows -1:
                self.text(other_lines, line + 1, align=align)
                
    def backlight(self, turn_on=True):
        self.backlight_status = turn_on
        self.write(0)
        
    def get_text_line(self, text):
        line_break = self.width
        if len(text) > self.width:
            line_break = text[:self.width + 1].rfind(' ')
        if line_break < 0:
            line_break = self.width
        return text[:line_break], text[line_break:].strip()
    
    def clear(self):
        self.write(CLEAR_DISPLAY)
        
lcd = LCD()
ADDRESS = 0x27

#initialize the interface of i2c
bus = smbus.SMBus(1)

#initial score
player1_score = 501
player2_score = 501
    
def update_scores():
    #update the score
    player1_score_str = str(player1_score)
    player2_score_str = str(player2_score)
    
    lcd.text("Player 1: " + player1_score_str, 1)
    lcd.text("Player 2: " + player2_score_str, 2)
running = True

while running:
    #display original score
    update_scores()

    #waiting time
    sleep(0.5)

    #sensor detected
    player1_score -= 100
    player2_score -= 19
    
    #update score and display
    update_scores()
    
    #waiting time
    sleep(0.5)
    
    if player1_score <= 0:
        if player1_score < 0:
            lcd.text("Player1 BUST!!!", 1)
        else:
            lcd.text("Player1 wins!!!", 1)
    
    if player2_score <= 0:
        if player2_score < 0:
            lcd.text("Player2 BUST!!!", 1)
        else:
            lcd.text("Player2 wins!!!", 1)  
            
    if player1_score <= 0 or player2_score <= 0:
        running = False
    
    lcd.clear()

#RB setting
    
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
button = 23
GPIO.setup(button, GPIO.OUT)
for i in range(3):
    time.sleep(1)
    if GPIO.input(button) == GPIO.HIGH:
        lcd.text("Game restart", 1)
        sleep(1)
        lcd.text("Player1: 501", 1)
        lcd.text("Player2: 501", 2)
        sleep(1)
        lcd.clear()
    else:
        lcd.text("Game Continue", 1)
        sleep(1)
        lcd.clear()
    
#NPB setting
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
button = 18
GPIO.setup(button, GPIO.OUT)
for i in range(6):
    time.sleep(1)
    if GPIO.input(button) == GPIO.HIGH:
        lcd.text("Switch to " , 1)
        lcd.text("Player2 " , 2)
        sleep(1)
        lcd.text("Player1: 501", 1)
        lcd.text("Player2: 501", 2)
        sleep(1)
        
        lcd.clear()
    else:
        lcd.text("Game~~~~", 1)
        sleep(1)
        lcd.clear()