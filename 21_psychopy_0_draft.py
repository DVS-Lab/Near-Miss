from psychopy import visual, core, gui, data, event, logging
import csv
import datetime
import random
import numpy
import os

"""Run 1 Time"""

#parameters
useFullScreen = True
DEBUG = False


#Get player ID
playerDlg = gui.Dlg(title = "21 Game Version 2")
playerDlg.addField('Enter Subject ID: ')
playerDlg.show()
player_id=playerDlg.data[0]

#open file to write to
f = open('subject_' + str(player_id) + '_data.csv', 'a+')
header = 'Trial_Number, Trial_Type, Bet, Wallet, Win_or_Loss, Number of Hits, Difference, Confidence Level, excited, proud, strong, nervous, distressed, ashamed \n'
f.write(header)

#Set up windows and ratings scales
win = visual.Window([1200,900], monitor = 'testMonitor')#, fullscr = useFullScreen)

#Instructions Screen
instructions_p1 = 'Welcome to 21. In this game, you will start with $5 in your wallet and will have the opportunity to let that amount grow, depending on how well you play the game. Press spacebar to continue.' 
instructions_p2 = 'In this game, you will be playing against the computer. Your goal in the game is to get closer to 21 than the computer without going over. Press spacebar to continue.' 
instructions_p3 = 'You will randomly be assigned 2 "cards". You have the option to hit (get another card value) or stay (not get another card value. The computer will stop "hitting" once its cards is greater than or equal to 14. Press spacebar to continue.'
instructions_p4 = 'Before you start playing the game, you will be asked to bet an amount. Your bet value has to be less than what\'s in your wallet and an integer value. Press the spacebar to continue.'
instructions_screen_p1 = visual.TextStim(win, font = 'Arial', text = instructions_p1)
instructions_screen_p1.draw()
win.flip()
event.waitKeys(keyList = ('space'))
instructions_screen_p2 = visual.TextStim(win, font = 'Arial', text = instructions_p2)
instructions_screen_p2.draw()
win.flip()
event.waitKeys(keyList = ('space'))
instructions_screen_p3 = visual.TextStim(win, font = 'Arial', text = instructions_p3)
instructions_screen_p3.draw()
win.flip()
event.waitKeys(keyList = ('space'))
instructions_screen_p4 = visual.TextStim(win, font = 'Arial', text = instructions_p4)
instructions_screen_p4.draw()
win.flip()
event.waitKeys(keyList = ('space'))

wallet = 5
#Main Loop
for i in range(1, 11):
    win.flip()
    #Place bet 
    bettingDlg = gui.Dlg(title = 'Please place your bet')
    bettingDlg.addFixedField('This is the amount of money in your wallet:', wallet)
    bettingDlg.addField('Bet Amount: ')
    bettingDlg.addFixedField('Game Number: ', i)
    bettingDlg.show()
    bet = int(bettingDlg.data[1])
    
    #Print out Computer's Cards
    computers_cards = []
    while sum(computers_cards) < 14:
        computers_cards.append(random.randint(1,10))
    card_output = 'The computer has ' + str(len(computers_cards)) + ' cards and one of those cards has a value of ' + str(computers_cards[0])
    computers_cards_screen = visual.TextStim(win, font = 'Arial', text = card_output)
    computers_cards_screen.draw()
    win.flip()
    core.wait(5.0)
    
    #Print out player's initial cards
    players_cards = []
    while len(players_cards) < 2:
        players_cards.append(random.randint(1,10))
    player_output = 'These are your cards: ' + str(players_cards)
    players_cards_screen = visual.TextStim(win, font = 'Arial', text = player_output)
    players_cards_screen.draw()
    win.flip()
    #event.waitKeys()
    k = ['']
    while sum(players_cards) < 21:
        hit_or_stay_text = player_output + '\nDo you want to hit (h) or stay (s)?'
        hit_or_stay_screen = visual.TextStim(win, font = 'Arial', text = hit_or_stay_text)
        # Break out hit loop
        if 's' in k:
            break
        # Get user input (h or s)
        k = ['']
        while k[0] not in ['h', 's']:
            hit_or_stay_screen.draw()
            win.flip()
            k = event.waitKeys()
            # Hit or Stay Logic
            if 'h' in k:
                # do hit logic, visual stuff here
                players_cards.append(random.randint(1,10))
                player_output = 'These are your cards: ' + str( players_cards)
                players_cards_screen = visual.TextStim(win, font = 'Arial', text = player_output)
                players_cards_screen.draw()
                win.flip()
            elif 's' in k: 
                win.flip()
                break

    #Losses
    if sum(players_cards) != 21 and sum(computers_cards) == 21:
        winning = 0
        computer_21_text = 'Computer got 21. \nThese are the computer\'s cards: ' + str(computers_cards) + '\nThese are your card\'s: ' + str(players_cards)
        computer_21_screen = visual.TextStim(win, font = 'Arial', text = computer_21_text)
        wallet = wallet - bet
        computer_21_screen.draw()
        win.flip()
    if sum(players_cards) > 21 and sum(computers_cards) < 21:
        winning = 0
        player_busts_text = 'You went over 21. \nThese are the computer\'s cards: ' + str(computers_cards)
        player_busts_screen = visual.TextStim(win, font = 'Arial', text = player_busts_text)
        wallet = wallet - bet
        player_busts_screen.draw()
        win.flip()
    if sum(players_cards) > 21 and sum(computers_cards) > 21:
        winning = 0
        player_and_computer_busts_text = 'You and the computer went over 21. You lose. \nThese are the computer\'s cards: ' + str(computers_cards)
        print(player_and_computer_busts_text)
        player_and_computer_busts_screen = visual.TextStim(win, font = 'Arial', text = player_and_computer_busts_text)
        wallet = wallet - bet
        player_and_computer_busts_screen.draw()
        win.flip()
    if sum(players_cards) < 21:
        #Losses
        if sum(players_cards) < sum(computers_cards) and sum(computers_cards) < 21:
            winning = 0
            computer_beat_player_text = 'The computer beat you by ' + str(sum(computers_cards)-sum(players_cards)) + ' points. \nThese are the computer\'s cards: ' + str(computers_cards)
            computer_beat_player_screen = visual.TextStim(win, font = 'Arial', text = computer_beat_player_text)
            wallet = wallet - bet
            computer_beat_player_screen.draw()
            win.flip()
        #Draw
        if sum(players_cards) == sum(computers_cards):
            winning = 1
            computer_tie_player_text = ' You and the computer tied.It\'s a draw. \nThese are the computer\'s cards: ' + str(computers_cards)
            computer_tie_player_screen = visual.TextStim(win, font = 'Arial', text = computer_tie_player_text)
            wallet = wallet
            computer_tie_player_screen.draw()
            win.flip()
        #Wins
        if sum(computers_cards) > 21:
            winning = 2
            computer_busts_text = 'The computer went over 21. You win. \nThese are the computer\'s cards: ' + str(computers_cards)
            computer_busts_screen = visual.TextStim(win, text = computer_busts_text)
            wallet = wallet + bet
            computer_busts_screen.draw()
            win.flip()
        elif sum(players_cards) > sum(computers_cards):
            winning = 2
            player_beat_computer_text = 'You beat the computer by ' + str(sum(players_cards)-sum(computers_cards)) + ' points. \nThese are the computer\'s cards: ' + str(computers_cards)
            player_beat_computer_screen = visual.TextStim(win, text = player_beat_computer_text, font = 'Arial')
            wallet = wallet + bet
            player_beat_computer_screen.draw()
            win.flip()
    #Win
    if sum(players_cards) == 21 and sum(computers_cards) != 21:
        winning = 2
        player_21_text = 'You got 21.\nThese are the computer\'s cards: ' + str(computers_cards)
        player_21_screen = visual.TextStim(win, font = 'Arial', text = player_21_text)
        wallet = wallet +  bet
        player_21_screen.draw()
        win.flip()
    #Draw
    if sum(players_cards) == 21 and sum(computers_cards) == 21:
        winning = 1
        player_and_computer_21_text = 'You and the computer got 21. It\'s a draw. \nThese are the computer\'s cards: ' + str(computers_cards)
        player_and_computer_21_screen = visual.TextStim(win, font = 'Arial', text = player_and_computer_21_text)
        wallet = wallet
        player_and_computer_21_screen.draw()
        win.flip()
    event.waitKeys(keyList = 'space')
    game_type = 0
    conf_level_response = 0
    excited_response = 0
    proud_response = 0
    strong_response = 0
    nervous_response = 0
    distressed_response = 0
    ashamed_response = 0
    data_to_write = str(i) + ',' + str(game_type) + ',' + str(bet)+ ',' + str(wallet) + ',' + str(winning) + ',' + str(len(players_cards)-2) + ',' + str(conf_level_response) + ',' + str(excited_response) + ',' + str(proud_response) + ',' + str(strong_response) + ',' + str(nervous_response) + ',' + str(distressed_response)+ ',' + str(ashamed_response) + '\n'
    f.write(data_to_write)

#Exit Screen
exit = 'Thanks for playing this round. Please wait for directions from your researcher.'
exit_screen = visual.TextStim(win, font = 'Arial', text = exit)

win.close()
core.quit()