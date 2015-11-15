#!/usr/bin/env python

import sys
import os
import clap
import time
from xml.dom import minidom

def speak(string):
	if string!='':
		os.popen("espeak -a 150 -v en+f3 \""+string+"\"").read() # returning result

def parentNode(xmldoc, node):
	if node!=xmldoc.firstChild:
		return node.parentNode
	else:
		return node

##############################################################################

# get a menu node, read it's options, and return the new node navigated to
def readMenu(xmldoc, menu_node):
	speak("This is the " + menu_node.getAttribute("name") + " menu.")
	speak(menu_node.getAttribute("value"))

	time.sleep(1)

	# the following loop print all the child nodes(which are the current menu)
	for child in menu_node.childNodes:
		if isinstance(child,minidom.Element):
			speak(child.getAttribute("name"))
			count=clap.listenAndCount(2)
			if count==1:
				return child
			if count==2:
				return parentNode(xmldoc, menu_node)

	speak("Menu Over.")
	speak("Clap to repeat")
	if menu_node!=xmldoc.firstChild:
		speak("Or clap twice to go back")
	
	claps=clap.waitForClaps()
	if claps>=2:
		return parentNode(xmldoc, menu_node)
	return menu_node

##############################################################################

def readDish(xmldoc, dish_node):
	speak("You have chosen to cook a " + current.getAttribute("name") + " " + current.parentNode.getAttribute("name"))
	speak("Clap once to  start cooking.")
	speak("Clap twice to hear the ingredients list.")
	speak("Clap 3 times to return to the menu")

	claps=clap.listenAndCount(3)
	while (claps==0):
		speak("I didn't get it.")
		speak("Please clap again.")
		claps=clap.listenAndCount(3)

	if claps==1:
		return dish_node.getElementsByTagName('method')[0]
	elif claps==2:
		return dish_node.getElementsByTagName('ingredients')[0]
	# 3+
	return parentNode(xmldoc, dish_node)

###############################################################################

def readIngredients(xmldoc, ing_node):
	speak("For this dish, the necessary ingredients are:")
	items=ing_node.getElementsByTagName('item');
	for item in items:
		speak(item.getAttribute("amount") + " " + item.firstChild.nodeValue)
	time.sleep(1)
	return parentNode(xmldoc, ing_node)

###############################################################################

def readMethod(xmldoc, method_node):
	speak("The method steps will be read one by one.")
	speak("Clap once to move to the next")
	speak("Clap twice to return to the dish menu")
	time.sleep(1)

	steps=method_node.getElementsByTagName('step');
	for step in steps:
		speak(step.firstChild.nodeValue)
		claps=clap.waitForClaps()
		print "####################### claps: " + str(claps)
		if claps>1:
			return parentNode(xmldoc, method_node)

	time.sleep(1)

	speak("Clap twice to return to the dish menu")
	return parentNode(xmldoc, method_node)

##################################### MAIN ####################################

time.sleep(1)
speak("Good morning sir. I will assist you cooking.");
speak("This system is based on clapping.")
speak("for start, please clap")

while (clap.listenAndCount(3)==0):
	speak("I didn't get it.")
	speak("Please clap again.")

speak("Great.")
speak("From now on, clap when you want to enter a certain menu or dish.")
speak("You can clap twice to return to the previous menu.")
time.sleep(1)

xmldoc = minidom.parse('recipe.xml')

current = xmldoc.firstChild
# dishes = current.getElementsByTagName('dish');
# for dish in dishes:
# 	if dish.getAttribute("name")=="tomato":
# 		current=dish

while (1):
	if current.tagName=='menu':
		current=readMenu(xmldoc, current)
		continue
	elif current.tagName=='dish':
		current=readDish(xmldoc,current)
		continue
	elif current.tagName=='ingredients':
		current=readIngredients(xmldoc,current)
		continue
	elif current.tagName=='method':
		current=readMethod(xmldoc,current)
		continue
	else:
		print "Error in xml, " + current.tagName + "is not a menu nor a dish"
		break