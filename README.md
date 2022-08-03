# Libmelee-SSBM-AI
Super Smash Bros. Melee A.I. created using Libmelee and Python

## How does the example AI actually fight?
It mainly uses foxes downthrow and tech chases you to oblivion

## Dependencies
### Libmelee
Libmelee is the library required to run this code which can be found [here](https://github.com/altf4/libmelee). you can simply do a ```pip install melee``` to get this library
### GALE01r2
this file is the nessescary gecko codes for this to function properly. WARNING : This will not let you connect online to Online Slippi as the codes are for an older version of slippi
PLEASE REMEMBER TO BACKUP YOUR OLD SLIPPI GALE01r2 FILE!
### File
Not a dependecy but, when downloading this, make sure to change your path file

## What do the file do tho?
### Melee_Bot.py
This file is really just the 'tie everything together' file. It takes all the tools and puts them together and really is the driver for everything
### manager.py
This does some of the behind the scenes stuff mostly for setup. It handles everything mainly to do with the console to get the game setup and also to get the gamestate
### tactic.py
This drives what to do, or what 'tactic' to pick from. It is used to detect what the opponent is doing, what the bot is doing, and how to act.
### tech.py
This basically presses the buttons. Any tech that needs to be performed such as WaveDashing or Multishining is stored here. it sees what animation we are in and when to act next.

## Project Goal
The goal of this project is NOT actually to create the ultimate AI to take over the melee scene. That would, if anything, be a side effect of this project. The main goal of this project is to create tools for other developers to use in their respective smashbots. I am creating basic tools, such as a method that can make any character wavedash, for other developers to use and even modify when they create their renditions of the smashbot. My Smash Bot is just an example of what can be done, not nessecarily the best final product.

## Known Issues
Transition from isHumanDead to shouldBeOffensive is not that smooth

It is actually possible to break out of a techchase but not teching, need to update that logic

The bot does not handle being hit very well at all (or really at all)

The bots recovery is wonky. Jumping is a little weird
