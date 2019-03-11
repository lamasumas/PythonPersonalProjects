# -*- coding: utf-8 -*-
import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 100)

voices = engine.getProperty('voices')

engine.setProperty('voice', voices[2].id)

while True:
	text= raw_input("WHAT TO SAY: ")
	engine.say(text)
	engine.runAndWait()
