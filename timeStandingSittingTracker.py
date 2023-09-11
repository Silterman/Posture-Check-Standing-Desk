import time; import math; from copy import deepcopy
from win11toast import toast
import threading

stateTrans = {0:"sitting", 1:"standing"}; sitStandTracker = {0:1, 1:1}
startTimer = time.time(); hours = 0
h = ""

currentState = int(input("Are you sitting(0) or standing(1)?"))
newState = deepcopy(currentState)

toast(f"You are now {stateTrans[currentState]}.")

print("Enter 2 to quit.")

class KeyboardThread(threading.Thread):
    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return

def my_callback(inp):
    if inp == 2:
        quit()
    global newState
    #evaluate the keyboard input
    newState = int(inp)
    print('You Entered:', inp)

#start the Keyboard thread
kthread = KeyboardThread(my_callback)

while True:
    timeNow = int(math.floor(time.time()-startTimer)/30)
    #currently triggering every 6 seconds for testing purposes -> will change /6 to a ratio of my choosing later
    if timeNow > hours:
        hours += 1
        if hours > 1: #used to make the toast switch from singular h to plural hs
            h = "s"
        output = f"You've been {stateTrans[currentState]} for {timeNow}h{h}. "
        if currentState == 1 and sitStandTracker[0]*2 <= sitStandTracker[1]+time.time()-startTimer:
            output += " Consider sitting now."
        elif currentState == 0 and (sitStandTracker[0]+time.time()-startTimer)*2 >= sitStandTracker[1]:
            output += " Consider standing now."
        toast("Posture warning", output)
    if newState != currentState: #how do I change newstate from outside the loop??????
        sitStandTracker.update({currentState:sitStandTracker[currentState]+(time.time()-startTimer)}) #ammends time to ratio tracker
        startTimer = time.time(); hours = 0 #resetting start time and last standing/sitting duration
        currentState = deepcopy(newState)
        toast(f"You are now {stateTrans[currentState]}.")
