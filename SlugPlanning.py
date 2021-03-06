"""
    Authors: Ted Ikehara and Austin Yen
    Date: Jan 14, 2022

    Main File: This program takes in data and allows the user to optimize their
    decision on what class to take.

    About: This project is for CruzHacks 2022. This is an academic planner
    aiming to help decrease the stress levels of students at University when
    picking classes.
"""

import platform
import copy
import os
from itertools import combinations

print('Loading...')
import slugplanningdb as sdb

if platform.system() == 'Linux' or platform.system() == 'Darwin':  # Checks the user's OS
    clearscreen = 'clear'
else:
    clearscreen = 'cls'

os.system(clearscreen)
print('Finished loading!')


def main():
    # User info
    currentQuarter = ''
    currentDiff = ''
    classTakenList = []
    canTakeClasses = []

    # system temp vars
    tmpString = ''
    tmpInt = 0
    tmpBool = True

    # l2 is subset of l1
    def sub_set(l1, l2):
        tmp = l2[:]
        for i in l1:
            if i in l1:
                if i in tmp:
                    tmp.remove(i)
                else:
                    return False
        return True

    def geReq():
        ge_req = ['cc', 'er', 'im', 'mf', 'si', 'sr', 'ta', 'pee', 'pre', 'c', 'dc']

        with open('classes.txt') as f:
            classTakenList = f.read().splitlines()

        ge_taken = []
        for i in sdb.CLASSES.keys():
            ge_taken.append(sdb.CLASSES.get(i).get("ge_satis"))
        ge_taken_parsed = [j for i in ge_taken for j in i]

        ge_needed = [x for x in ge_req if x not in ge_taken_parsed]
        if not ge_needed:
            print('You satisfied all GEs')
        else:
            print('GE categories needed: ', ge_needed)

    # greetings and main function

    print("Welcome to the SlugPlanner!")

    # Asking student current quarter

    tmpString = 'n'
    while tmpString == 'n':
        currentQuarter = input('What is your current quarter? (Fall, Winter, Spring, Summer): ').title()
        print('Your current quarter is: ', currentQuarter)
        print('Is this correct?: ')

        tmpString = input('type y or n... ')
        if tmpString != 'y' and tmpString != 'n':
            print('Invalid response, try again')
            continue

    # Asking student difficulty of classes
    print('How are you managing your classes so far?: ')
    currentDiff = input('Type, E (Easy Course Load), M (Medium Course Load), H (Hard Course Load): ').lower()  # Check invalid response?
    print('Your current difficulty is set to:', currentDiff)

    # from txt file classes and appending to the canTakeClasses
    print('Accessing text file... \n')
    with open('classes.txt') as f:
        classTakenList = f.read().splitlines()

    # appending classes to can take classes
    for i in sdb.CLASSES.keys():

        if sub_set(sdb.CLASSES.get(i).get("prereqs"), classTakenList):
            if currentQuarter in sdb.CLASSES.get(i).get("quarter_offered"):
                canTakeClasses.append(i)

    print('Classes that you already took: ', *classTakenList)

    # generating combinations of the classes that you can take
    classTaken = []
    for i in classTakenList:
        classTaken.append(i)

    tmpA = classTakenList
    tmpB = canTakeClasses

    tmpC = []

    for elem in copy.deepcopy(tmpA):
        if elem in tmpB:
            tmpA.pop(tmpA.index(elem))
            tmpC.append(tmpB.pop(tmpB.index(elem)))

    print('Classes you can take: ', *canTakeClasses)

    # shows what GEs you still need
    geReq()

    nc = True
    numClass = 0
    while nc:
        numClass = int(input('Choose the amount of classes you want to take next quarter: '))
        if numClass > len(canTakeClasses):
            print("Not enough available classes to take, please try again")
            continue
        if numClass > 4:
            print("You can't take 5 classes, you will die")
            continue
        nc = False

    count = 0
    possibleClasses = []

    print('\nYour possible options: ')
    for i in combinations(canTakeClasses, numClass):
        print(count, '. ', i)

        tmpDiff = []

        # printing out all the class options
        print('The difficulty of these classes: ', end='')
        for j in i:
            diff = sdb.CLASSES.get(j).get('difficulty')
            print(diff, ', ', end='')
            tmpDiff.append(diff)

        diffAvg = sum(tmpDiff) / len(tmpDiff)
        print('\nThe average difficulty is: {:.2f}\n'.format(diffAvg))

        possibleClasses.append(i)
        count += 1

    if currentDiff == 'e':
        print('Your recommended difficulty is: 7-10')
    if currentDiff == 'm':
        print('Your recommended difficulty is: 4-6')
    if currentDiff == 'h':
        print('Your recommended difficulty is: 1-3')

    # generated list of your preffered schedule
    tmpInt = int(input('\nChoose by number your preferred schedule: '))
    plan = possibleClasses[tmpInt]

    os.system(clearscreen)

    # all the stats
    def stats(cl, inpu):
        return sdb.CLASSES.get(cl).get(inpu)

    # entering command line
    while True:

        print('Your planned classes: ', plan)

        user = input('Type commands: ')

        if user == 'stats':
            os.system(clearscreen)

            # flipboard for planned classes

            bo = True
            i = 0

            while bo:

                print('Stats of classes: ')
                print('Your planned classes: ', plan)
                print('class ', i + 1, '/', len(plan))
                print(plan[i])
                print('Can you get this class rating: ', stats(plan[i], 'availability'))
                print('General discription of this class: ', stats(plan[i], 'gen_descrip'))
                print('The difficulty of this class is: ', stats(plan[i], 'difficulty'))
                print('The syllabus of the class: ', stats(plan[i], 'syllabus'))
                print('The textbook of the class: ', stats(plan[i], 'textbook'))
                print('Does this class have a lab?: ', stats(plan[i], 'haslab'))
                print('Are the TAs helpful rating?: ', stats(plan[i], 'ta_helpful'))
                print('What is this class focusing on? 0:math, 1:coding, 2:other', stats(plan[i], 'class_type'))
                print('The time commitment rating out of three: ', stats(plan[i], 'time_commit'))
                print('Most people preffer: ', stats(plan[i], 'pref_prof'))

                op = input('\nPress k to go next, j to go back, any other key to return: ')

                if op == 'k':
                    i += 1
                if op == 'j':
                    i -= 1
                if i >= len(plan) or i <= len(plan):
                    i = i % len(plan)
                if not (op == 'j') and not (op == 'k'):
                    bo = False

                os.system(clearscreen)

                continue

        # gets info to any class
        if user == 'info':
            cl = input('Search Class: ')
            try:
                print(cl)
                print('Can you get this class rating: ', stats(cl, 'availability'))
                print('General discription of this class: ', stats(cl, 'gen_descrip'))
                print('The difficulty of this class is: ', stats(cl, 'difficulty'))
                print('The syllabus of the class: ', stats(cl, 'syllabus'))
                print('The textbook of the class: ', stats(cl, 'textbook'))
                print('Does this class have a lab?: ', stats(cl, 'haslab'))
                print('Are the TAs helpful rating?: ', stats(cl, 'ta_helpful'))
                print('What is this class focusing on? 0:math, 1:coding, 2:other', stats(cl, 'class_type'))
                print('The time commitment rating out of three: ', stats(cl, 'time_commit'))
                print('Most people preffer: ', stats(cl, 'pref_prof'))
            except:
                print('Invalid class... ')

        if user == 'help':
            print('-- stats: prints all the stats of your planned classes')
            print('-- info: gets info of any class')
            print('-- clear: clears the screen')
            print('-- generate: updates the classes.txt file with classes you chose and runs the program again')
            print('-- exit: quits program')
            print('-- help: displays commands')

        if user == 'generate':
            with open("classes.txt", "a") as f:
                for i in plan:
                    f.write(i + "\n")
            main()
        if user == 'clear':
            os.system(clearscreen)
        if user == 'exit':
            print('Goodbye :)')
            break


if __name__ == '__main__':
    main()
