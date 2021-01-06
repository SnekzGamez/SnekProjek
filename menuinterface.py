import csv
import sys

def main():
	menu()

def menu():
	print("******************** WELCOME TO SNEKZGAMEZ ********************")
	print()

	choice = input("""
			A: PLAY GAME
			B: VIEW SCOREBOARD

			Please enter your choice: """)

	if choice == "A" or choice == "a":


	elif choice == "B" or choice == "b":


	else:
		print("You must only select either A or B")
		print("Please try again!")
		menu()

#the program is initiated
main()
