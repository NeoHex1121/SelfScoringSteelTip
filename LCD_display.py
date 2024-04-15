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
current_player = 0

def update_score1():
    #update the score
    player1_score_str = str(player1_score)
    lcd.text("Player 1: " + player1_score_str, 1)
    
def update_score2():
    player2_score_str = str(player2_score)
    lcd.text("Player 2: " + player2_score_str, 2)
    
def RB():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    button = 23
    GPIO.setup(button, GPIO.OUT)
    if GPIO.input(button) == GPIO.HIGH:
        global player1_score, player2_score, current_player
        player1_score = 501
        player2_score = 501
        current_player = 0
        Dart_Count = 0
        player1_score_str = str(player1_score)
        player2_score_str = str(player2_score)
        lcd.clear()
        lcd.text("Game restart", 1)
        sleep(1)
        lcd.text("Player 1: " + player1_score_str, 1)
        lcd.text("Player 2: " + player2_score_str, 2)
        sleep(1)
        return True
    else:
        update_score1()
        update_score2()
        return False

def NPB():
    global player1_score, player2_score, current_player
    player1_score_str = str(player1_score)
    player2_score_str = str(player2_score)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    button = 18
    GPIO.setup(button, GPIO.OUT)
    if GPIO.input(button) == GPIO.HIGH:
        current_player = (current_player + 1) % 2
        if current_player == 0:
            lcd.text("Switch to " , 1)
            lcd.text("Player2 " , 2)
            sleep(1)
            lcd.text("Player 1: " + player1_score_str, 1)
            lcd.text("Player 2: " + player2_score_str, 2)
            sleep(1)
            lcd.clear()
            return True
        else:
            lcd.text("Switch to " , 1)
            lcd.text("Player1 " , 2)
            sleep(1)
            lcd.text("Player 1: " + player1_score_str, 1)
            lcd.text("Player 2: " + player2_score_str, 2)
            sleep(1)
            lcd.clear()
            return True
    else:
        update_score1()
        update_score2()
    
running = True

lcd.text("Welcome to the", 1)
lcd.text("Dartboard Game!", 2)
sleep(1)
lcd.clear()

while running:
    
    for i in range(3):
        update_score1()
        update_score2()
        current_player = 1
        sleep(1)
        player1_score -= 200
        player1_score_str = str(player1_score)
        player2_score_str = str(player2_score)
        lcd.text("->Player 1: " + player1_score_str, 1)
        lcd.text("Player 2: " + player2_score_str, 2)
        sleep(1)
        if RB():
            for i in range(3):
                update_score1()
                update_score2()
                current_player = 1
                sleep(1)
                player1_score -= 50
                player1_score_str = str(player1_score)
                player2_score_str = str(player2_score)
                lcd.text("->Player 1: " + player1_score_str, 1)
                lcd.text("Player 2: " + player2_score_str, 2)
                sleep(1)
                if NPB():
                    break
                if player1_score or player2_score <= 0:
                    if player1_score < 0:
                        lcd.clear()
                        lcd.text("Player1 BUST!!!", 1)
                        sleep(1)
                        running = False
                        break
                    elif player1_score == 0:
                        lcd.clear()
                        lcd.text("Player1 wins!!!", 1)
                        sleep(1)
                        running = False
                        break
                    elif player2_score < 0:
                        lcd.clear()
                        lcd.text("Player2 BUST!!!", 1)
                        sleep(1)
                        running = False
                        break
                    elif player2_score == 0:
                        lcd.clear()
                        lcd.text("Player2 wins!!!", 1)
                        sleep(1)
                        running = False
                        break
            break
        
        if NPB():
            break
        
        if player1_score or player2_score <= 0:
            if player1_score < 0:
                lcd.clear()
                lcd.text("Player1 BUST!!!", 1)
                sleep(1)
                running = False
                break
            elif player1_score == 0:
                lcd.clear()
                lcd.text("Player1 wins!!!", 1)
                sleep(1)
                running = False
                break
            elif player2_score < 0:
                lcd.clear()
                lcd.text("Player2 BUST!!!", 1)
                sleep(1)
                running = False
                break
            elif player2_score == 0:
                lcd.clear()
                lcd.text("Player2 wins!!!", 1)
                sleep(1)
                running = False
                break 
        
    for j in range(3):
        update_score1()
        update_score2()
        current_player = 2
        sleep(1)
        player2_score -= 167
        player1_score_str = str(player1_score)
        player2_score_str = str(player2_score)
        lcd.text("Player 1: " + player1_score_str, 1)
        lcd.text("->Player 2: " + player2_score_str, 2)
        sleep(1)
        if RB():
            break
        if NPB():
            break
        if player1_score or player2_score <= 0:
            if player1_score < 0:
                lcd.clear()
                lcd.text("Player1 BUST!!!", 1)
                sleep(1)
                running = False
                break
            elif player1_score == 0:
                lcd.clear()
                lcd.text("Player1 wins!!!", 1)
                sleep(1)
                running = False
                break
            elif player2_score < 0:
                lcd.clear()
                lcd.text("Player2 BUST!!!", 1)
                sleep(1)
                running = False
                break
            elif player2_score == 0:
                lcd.clear()
                lcd.text("Player2 wins!!!", 1)
                sleep(1)
                running = False
                break
    
    lcd.clear()
    
