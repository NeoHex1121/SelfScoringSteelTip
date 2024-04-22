#from gpiozero import
import RPi.GPIO as GPIO
import time
import math
#use GPIO pins 11 5 6 13 19 26 as C_sel.  These are not the physical pin numbers but the "GPIO" pin numbers
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
MAX_DART_SCORE = 60
A71 = 3
A72 = 5
CS7 = 7
A73 = 13
A74 = 11
GPIO.setup(A71, GPIO.IN)
GPIO.setup(A72, GPIO.IN)
GPIO.setup(CS7, GPIO.IN)
GPIO.setup(A73, GPIO.IN)
GPIO.setup(A74, GPIO.IN)
x_channel = []
x_fpga = []
y_channel = []
y_fpga = []

count=0
C_sel0_pin= 8
GPIO.setup(C_sel0_pin, GPIO.OUT)
C_sel1_pin= 10
GPIO.setup(C_sel1_pin, GPIO.OUT)
C_sel2_pin= 12
GPIO.setup(C_sel2_pin, GPIO.OUT)
C_sel3_pin= 16
GPIO.setup(C_sel3_pin, GPIO.OUT)
C_sel4_pin= 18
GPIO.setup(C_sel4_pin, GPIO.OUT)
C_sel5_pin= 22
GPIO.setup(C_sel5_pin, GPIO.OUT)
X=1

def get_player_input(player_name, dart_number,base_score):
        print (f"{player_name}, Please toss a dart or Type 'Next' to move on")
        base_score = input(message).lower()
        base_score = 0
        if dart_input == 'next':
            return 0
def update_score(player, points):
    player['score'] = max(0, player['score'] - points)

def check_winner(player):
    return player['score'] == 0

def print_scores(player1, player2):
    print(f"\nCurrent Scores - {player1['name']}: {player1['score']} | {player2['name']}: {player2['score']}")

def player_turn(player):
    initial_score = player['score']
    total_points = 0

    print(f"\n{player['name']}'s Turn:")
    for dart_number in range(1, 4):
        base_score = get_player_input(player['name'], dart_number)
        total_points += base_score
        print(f"{player['name']}, Dart {dart_number}: {'Next' if dart_score == 0 else dart_score}")

        if player['score'] - total_points < 0:
            print(f"{player['name']} busts! Resetting score for this turn.")
            player['score'] = initial_score
            return

    update_score(player, total_points)
    
def main():
    storex=0
    storey=0
    domath=0
    players = [{"score": 501, "name": "Player 1"}, {"score": 501, "name": "Player 2"}]
    print("Welcome to the 501 Dart Game!")
    current_player = 0
    while True:

        for i in range(37):
            time.sleep(0.2)
    #         count=(0.2)
            binary_list = (list(bin(i)[2:].zfill(6)))
            current_binary=binary_list
            if i == 37:
                i == 0
            
            
        
            if  eval(binary_list[5])==1:
                GPIO.output(C_sel0_pin, GPIO.HIGH)
            if eval(binary_list[5])==0:
                GPIO.output(C_sel0_pin, GPIO.LOW)
        
            if  eval(binary_list[4])==1:
                GPIO.output(C_sel1_pin, GPIO.HIGH)
            if eval(binary_list[4])==0:
                GPIO.output(C_sel1_pin, GPIO.LOW)
            if  eval(binary_list[3])==1:
                GPIO.output(C_sel2_pin, GPIO.HIGH)
            if eval(binary_list[3])==0:
                GPIO.output(C_sel2_pin, GPIO.LOW)
            if  eval(binary_list[2])==1:
                GPIO.output(C_sel3_pin, GPIO.HIGH)
            if eval(binary_list[2])==0:
                GPIO.output(C_sel3_pin, GPIO.LOW)
            if  eval(binary_list[1])==1:
                GPIO.output(C_sel4_pin, GPIO.HIGH)
            if eval(binary_list[1])==0:
                GPIO.output(C_sel4_pin, GPIO.LOW)
            if  eval(binary_list[0])==1:
                GPIO.output(C_sel5_pin, GPIO.HIGH)
            if eval(binary_list[0])==0:
                GPIO.output(C_sel5_pin, GPIO.LOW)
            if (GPIO.input(A71))  == 0:
                y_channel = i
                y_fpga = A71
                storey=1
                y=y_channel
              
            if(GPIO.input(A72)) == 0:
                y_channel = i
                y_fpga = A72
                storey=1
                y=36+y_channel
            if(GPIO.input(A73)) == 0:
                x_channel = i
                x_fpga = A73
                storex=1
                x=x_channel
            if(GPIO.input(A74))  == 0:
                x_channel = i
                x_fpga = A74
                storex=1
                x=x_channel+36
                
            if(GPIO.input(CS7))  == 0:
                x_channel = i
                x_fpga = CS7
                storex=1
                72+x_channel
            if storey and storex==1:
                print ('y channel is:',y_channel,'y fpga is:', y_fpga,'x channel is:', x_channel,'x fpga is:', x_fpga)
                domath=1
            if domath==1:
                
                print('math done')
                print('xcord=',x)
                print('ycord=',y)
                r = math.sqrt(x**2 + y**2)
                θ = math.degrees(math.atan2(y, x)) % 360
                print (r, θ)
                TRIPLE_START, TRIPLE_END = 99, 107
                DOUBLE_START, DOUBLE_END = 162, 170
                OUTER_BULL, INNER_BULL = 25, 12.7
        
                SEGMENT_SCORES = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]
        
                segment_index = int(θ // 18)
                base_score = SEGMENT_SCORES[segment_index]
                if r <= INNER_BULL==0:
                    print ('in,',50)
                elif r <= OUTER_BULL:
                    print ('out,',25)
                elif TRIPLE_START <= r <= TRIPLE_END:
                    print ('tripple,',base_score * 3)
                elif DOUBLE_START <= r <= DOUBLE_END:
                    print ('double,',base_score * 2)
                elif r <= DOUBLE_START:
                    print ('base score',base_score)
                else:
                    print (0)
                return base_score
                storex=0
                storey=0
                domath=0
                print (f"{player_name}, Please toss a dart or Type 'Next' to move on")
                base_score = input(message).lower()
                base_score = 0
                if dart_input == 'next':
                    return 0
            else:
                time.sleep(0.2)
                
        print_scores(players[0], players[1])
        player_turn(players[current_player])

        if check_winner(players[current_player]):
            print(f"\nCongratulations, {players[current_player]['name']} wins!")
            break

        current_player = 1 - current_player
        
                
if __name__ == "__main__":
    main()
            
            
