from psychopy import visual, core, gui, data, event, logging
import csv
import datetime
import random
import numpy
import os

win = visual.Window([800,600], monitor = 'testMonitor')

#Get player ID
playerDlg = gui.Dlg(title = '21 Pre-Game Survey')
playerDlg.addField('Enter Subject ID: ')
playerDlg.show()
player_id=playerDlg.data[0]

f = open('subject_' + str(player_id) +'_presurvey.csv', 'a+') 
header = ('question 1' + ',' + 'question_2' + ',' + 'question_3')

question_1 = visual.RatingScale(win, low = 1, high = 5, markerStart = 3, leftKeys = 'left', rightKeys = 'right', acceptKeys = 'space' )
question_1_text = visual.TextStim(win, font = 'Arial', text = 'Choose one of the following answers: \n A) 10% \n B) 80% \n C) 30% \n D) 50% \n E) Don\'t Know')
question_1_text.draw()
question_1.draw()
win.flip()
question_1_answer = question_1.getRating()
if question_1_answer == 3:
    q1 = 1
else:
    q1 = 2

question_2 = visual.RatingScale(