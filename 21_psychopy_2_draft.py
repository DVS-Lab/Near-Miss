from psychopy import visual, core, gui, data, event, logging
import csv
import datetime
import random
import numpy
import os

"""Run 3 Times"""

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
for i in range(1, 31):
    if i == 11 or i == 21:
        wallet = 5
        new_game_text = 'You will start the next round of this game. Same rules apply. You will now start with $5 in your wallet again. Press spacebar to continue.'
        new_game_screen = visual.TextStim(win, font = 'Arial', text = new_game_text)
        new_game_screen.draw()
        win.flip()
        event.waitKeys(keyList = 'space')
    if i == 1 or i == 2 or i == 4 or i == 5 or i ==6 or i ==8 or i == 9 or i == 11 or i == 12 or i == 14 or i == 15 or i == 16 or i ==18 or i == 19 or i == 21 or i == 22 or i == 24 or i == 25 or i == 26 or i == 28 or i == 29:
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
        conf_level = 0
        excited = 0
        proud = 0
        strong = 0
        nervous = 0
        distressed = 0
        ashamed = 0


#Near Miss Codes
    if i == 3 or i == 8 or i == 13 or i == 18 or i == 23 or i == 28:
        #Define ratings scale screen
        winning = 0
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
            computers_cards.append(random.randint(7,10))
        card_output = 'The computer has ' + str(3) + ' cards and one of those cards has a value of ' + str(computers_cards[0])
        computers_cards_screen = visual.TextStim(win, font = 'Arial', text = card_output)
        computers_cards_screen.draw()
        win.flip()
        core.wait(5.0)
        
        #Print out player's initial cards
        players_cards = []
        while len(players_cards) < 2:
            players_cards.append(random.randint(7,10))
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
                    if sum(players_cards) < 17:
                        players_cards.append(random.randint(1,3))
                    if sum(players_cards) == 17 or sum(players_cards) == 18:
                        players_cards.append(2)
                    if sum(players_cards) == 19:
                        players_cards.append(1)
                    if sum(players_cards) == 20:
                        players_cards.append(2)
                    player_output = 'These are your cards: ' + str( players_cards)
                    players_cards_screen = visual.TextStim(win, font = 'Arial', text = player_output)
                    players_cards_screen.draw()
                    win.flip()
                elif 's' in k: 
                    message = 'These are your cards: ' + str( players_cards)
                    message_screen = visual.TextStim(win, text = message)
                    message_screen.draw()
                    win.flip()
                    break
        #Losses
        if sum(players_cards) != 21 and sum(computers_cards) == 21:
            winning = 0
            computer_21_text = 'Computer got 21. \nThese are the computer\'s cards: ' + str(computers_cards) + '\nThese are your cards: ' + str(players_cards)
            player_busts_screen = visual.TextStim(win, font = 'Arial', text = computer_21_text)
            wallet = wallet - bet
            player_busts_screen.draw()
            win.flip()
            core.wait(5.0)
        if sum(players_cards) > 21:
            winning = 0
            del computers_cards[1]
            computers_cards.append(int((22-sum(computers_cards))/2))
            computers_cards.append(19-sum(computers_cards))
            player_busts_text = 'You went over 21. \nThese are the computer\'s cards: ' + str(computers_cards) + '\nThese are your cards: ' + str(players_cards)
            player_busts_screen = visual.TextStim(win, font = 'Arial', text = player_busts_text)
            wallet = wallet - bet
            player_busts_screen.draw()
            win.flip()
            core.wait(5.0)

        if sum(players_cards) < 21:
            #Losses
            winning = 0
            del computers_cards[1]
            computers_cards.append(int((sum(players_cards)-sum(computers_cards))/2)) 
            computers_cards.append((sum(players_cards)-sum(computers_cards)+1))
            computer_beat_player_text = 'The computer beat you by ' + str(sum(computers_cards)-sum(players_cards)) + ' points. \nThese are the computer\'s cards: ' + str(computers_cards) + '\nThese are your cards: ' + str(players_cards)
            computer_beat_player_screen = visual.TextStim(win, font = 'Arial', text = computer_beat_player_text)
            wallet = wallet - bet
            computer_beat_player_screen.draw()
            win.flip()
            core.wait(5.0)
        win.flip()
#Ratings Scale
    if i == 1 or i == 4 or i == 7 or i == 10 or i == 11 or i == 14 or i == 17 or i == 20 or i == 21 or i == 24 or i == 27 or i == 30:
        conf_level = visual.RatingScale(win, low = 1, high = 5, markerStart = 3, leftKeys = '1', rightKeys = '3', acceptKeys = '2')
        excited = visual.RatingScale(win, low = 1, high = 5, markerStart = 3, leftKeys = '1', rightKeys = '3', acceptKeys = '2')
        proud = visual.RatingScale(win, low = 1, high = 5, markerStart = 3, leftKeys = '1', rightKeys = '3', acceptKeys = '2')
        strong = visual.RatingScale(win, low = 1, high = 5, markerStart = 3, leftKeys = '1', rightKeys = '3', acceptKeys = '2')
        nervous = visual.RatingScale(win, low = 1, high = 5, markerStart = 3, leftKeys = '1', rightKeys = '3', acceptKeys = '2')
        distressed = visual.RatingScale(win, low = 1, high = 5, markerStart = 3, leftKeys = '1', rightKeys = '3', acceptKeys = '2')
        ashamed = visual.RatingScale(win, low = 1, high = 5, markerStart = 3, leftKeys = '1', rightKeys = '3', acceptKeys = '2')
        ratings_instruction = 'This scale consists of a number of words that describe different feelings and emotions. \nRead each item and rate on a scale of 1-5 the extent to which you feel this way in this moment.\n 1 represents \'very slightly or not at all\' while 5 represents \'extremely\'.\nPress the spacebar to continue'
        ratings_screen = visual.TextStim(win, font = 'Arial', text = ratings_instruction)
        ratings_screen.draw()
        win.flip()
        event.waitKeys(keyList = 'space')
        
        while conf_level.noResponse:
            conf_level_text = 'How confident are you with your 21 playing abilities?'
            conf_level_screen = visual.TextStim(win, font = 'Arial', text = conf_level_text)
            conf_level_screen.draw()
            conf_level.draw()
            win.flip()
        conf_level_response = conf_level.getRating()
        while excited.noResponse:
            excited_screen = visual.TextStim(win, font = 'Arial', text = 'Excited')
            excited_screen.draw()
            excited.draw()
            win.flip()
        excited_response = excited.getRating()
        while proud.noResponse:
            proud_screen = visual.TextStim(win, font = 'Arial', text = 'Proud')
            proud_screen.draw()
            proud.draw()
            win.flip()
        proud_response = proud.getRating()
        while strong.noResponse:
            strong_screen = visual.TextStim(win, font = 'Arial', text = 'Strong')
            strong_screen.draw()
            strong.draw()
            win.flip()
        strong_response = strong.getRating()
        while nervous.noResponse:
            nervous_screen = visual.TextStim(win, font = 'Arial', text = 'Nervous')
            nervous_screen.draw()
            nervous.draw()
            win.flip()
        nervous_response = nervous.getRating()
        while distressed.noResponse:
            distressed_screen = visual.TextStim(win, font = 'Arial', text = 'Distressed')
            distressed_screen.draw()
            distressed.draw()
            win.flip()
        distressed_response = distressed.getRating()
        while ashamed.noResponse:
            ashamed_screen = visual.TextStim(win, font = 'Arial', text = 'Ashamed')
            ashamed_screen.draw()
            ashamed.draw()
            win.flip()
        ashamed_response = ashamed.getRating()
        game_type = 1
    data_to_write = str(200+i) + ',' + str(game_type) + ',' + str(bet)+ ',' + str(wallet) + ',' + str(winning) + ',' + str(len(players_cards)-2) + ',' + str(conf_level_response) + ',' + str(excited_response) + ',' + str(proud_response) + ',' + str(strong_response) + ',' + str(nervous_response) + ',' + str(distressed_response)+ ',' + str(ashamed_response) + '\n'
    f.write(data_to_write)

#Exit Screen
exit = 'Thanks for playing this round. Please wait for directions from your researcher.'
exit_screen = visual.TextStim(win, font = 'Arial', text = exit)

win.close()
core.quit()