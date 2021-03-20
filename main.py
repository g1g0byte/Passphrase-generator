import csv,random
from tkinter import *

def read_words_file():
	words_list = {}
	with open('words.csv', 'r') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			words_list.update({row[0]:row[1]})
	return words_list

def create_passphrase(words_list,amount_of_words,should_space_words, should_capitalise, should_random_numbers):
	# Create list of random word codes
	word_codes=[]
	for i in range(amount_of_words):
		word_code=''
		for i in range(5):
			roll = random.SystemRandom().randint(1, 6)
			word_code += str(roll)
		word_codes.append(word_code)

	# Find words that match the generated word codes
	selected_words=[]
	for i in range(len(word_codes)):
		# loop through each key in words_list to find matching word code
		if word_codes[i] in words_list.keys():
			selected_words.append(words_list[word_codes[i]])
		else:
			print("Problem occured with finding a word in list")
			quit()

	if (should_capitalise):
		for i in range(amount_of_words):
			selected_words[i] = selected_words[i].capitalize()
	
	numbers=['' for i in range(amount_of_words)]
	add_number_chance = 50	# chance of generating a number at end of each word
	if (should_random_numbers):
		for i in range(len(numbers)):
			chance = random.randint(1,100)
			if chance <= add_number_chance:
				numbers[i] = str(random.SystemRandom().randint(1, 6))

	if (should_space_words):
		space = ' '
	else:
		space = ''
	
	passphrase=''
	for i in range(amount_of_words):
		passphrase += selected_words[i]+numbers[i]+space
	
	passphrase_label = Label(root,text=passphrase)
	passphrase_label.grid()
	return passphrase

# main program
words_list = read_words_file()

# tkinter code
root = Tk()
root.title("Passphrase generator")
root.geometry("300x400") 

amount_of_words_title = Label(root,text="Amount of words:")
amount_of_words_inputfield = Entry(root,width=2)
amount_of_words_inputfield.insert(0, 4)

should_space_words = IntVar()
space_words_checkbutton = Checkbutton(root,text="Space between words",variable=should_space_words)
space_words_checkbutton.select()

should_capitalise = IntVar()
capitalise_checkbutton = Checkbutton(root,text="capitalise word",variable=should_capitalise)

should_random_numbers = IntVar()
random_numbers_checkbutton = Checkbutton(root,text="random numbers",variable=should_random_numbers)

generate_button = Button(root,text="Generate Passphrase",
command=lambda: create_passphrase(words_list,int(amount_of_words_inputfield.get()),should_space_words.get(),should_capitalise.get(), should_random_numbers.get()))


generate_button.grid(row=0)
amount_of_words_title.grid(row=1,column=0)
amount_of_words_inputfield.grid(row=1,column=1)
space_words_checkbutton.grid(row=2)
capitalise_checkbutton.grid(row=3)
random_numbers_checkbutton.grid(row=4)

root.mainloop()