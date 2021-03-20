import random, words_file
from tkinter import *

def create_passphrase(words_list,amount_of_words,should_space_words, should_capitalise, capitalise_letter_chance, should_random_numbers, add_number_chance):
	# create list of random word codes
	word_codes=[]
	for i in range(amount_of_words):
		word_code=''
		for i in range(5):
			roll = random.SystemRandom().randint(1, 6)
			word_code += str(roll)
		word_codes.append(word_code)

	# find words that match the generated word codes
	selected_words=[]
	for i in range(amount_of_words):
		# loop through each key in words_list to find matching word code
		if word_codes[i] in words_list.keys():
			selected_words.append(words_list[word_codes[i]])
		else:
			print("Problem occured with finding a word in list")
			quit()

	# capitalise letters in words if desired
	if (should_capitalise):
		for i in range(amount_of_words):
			for letter in selected_words[i]:
				chance = random.SystemRandom().randint(1, 100)
				if chance <= capitalise_letter_chance:
					selected_words[i] = selected_words[i].replace(letter,letter.upper())
	
	# generate random numbers to add to passphrase if desired
	numbers=['' for i in range(amount_of_words)]	# fill with blank strings incase user does not want numbers
	if (should_random_numbers):
		for i in range(amount_of_words):
			chance = random.SystemRandom().randint(1, 100)
			if chance <= add_number_chance:
				numbers[i] = str(random.SystemRandom().randint(1, 6))

	if (should_space_words):
		space = ' '
	else:
		space = ''
	
	passphrase=''
	for i in range(amount_of_words):
		passphrase += selected_words[i]+numbers[i]+space
	passphrase = passphrase.rstrip()	# remove last space at end of passphrase

	# replace current passphrase being displayed
	passphrase_text.delete(0, END)
	passphrase_text.insert(0, passphrase)

	# clear the users clipboard and add passphrase to it
	root.clipboard_clear()
	root.clipboard_append(passphrase)


def toggle_capitalise_chance(enabled):
	if (not enabled):
		capitalise_chance_title.configure(state='disabled')
		capitalise_chance_inputfield.configure(state='disabled')
	else:
		capitalise_chance_title.configure(state='normal')
		capitalise_chance_inputfield.configure(state='normal')

def toggle_add_number_chance(enabled):
	if (not enabled):
		add_number_chance_title.configure(state='disabled')
		add_number_chance_inputfield.configure(state='disabled')
	else:
		add_number_chance_title.configure(state='normal')
		add_number_chance_inputfield.configure(state='normal')

# tkinter code
root = Tk()
root.title("Passphrase generator")
root.geometry("400x500")

amount_of_words_title = Label(root,text="Amount of words:")
amount_of_words_inputfield = Entry(root,width=2)
amount_of_words_inputfield.insert(0, 4)

should_space_words = IntVar()
space_words_checkbutton = Checkbutton(root,text="Space between words",variable=should_space_words,width="20")
space_words_checkbutton.select()

should_capitalise = IntVar()
capitalise_checkbutton = Checkbutton(root,text="capitalise letters",variable=should_capitalise,width="20",command=lambda: toggle_capitalise_chance(should_capitalise.get()))
capitalise_checkbutton.select()

capitalise_chance_title = Label(root,text="Chance of each letter being capitalised:")
capitalise_chance_inputfield = Entry(root,width="3",justify='center')
capitalise_chance_inputfield.insert(0, 20)

should_random_numbers = IntVar()
random_numbers_checkbutton = Checkbutton(root,text="random numbers",variable=should_random_numbers,width="20",command=lambda: toggle_add_number_chance(should_random_numbers.get()))
random_numbers_checkbutton.select()

add_number_chance_title = Label(root,text="Generate number chance:")
add_number_chance_inputfield = Entry(root,width="3",justify='center')
add_number_chance_inputfield.insert(0, 50)

generate_button = Button(root,text="Generate Passphrase",
command=lambda: create_passphrase(words_list,int(amount_of_words_inputfield.get()),should_space_words.get(),should_capitalise.get(),int(capitalise_chance_inputfield.get()),should_random_numbers.get(),int(add_number_chance_inputfield.get())))

passphrase_text = Entry(root,justify='center',width=40)

passphrase_text.pack()
generate_button.pack()
amount_of_words_title.pack()
amount_of_words_inputfield.pack()
space_words_checkbutton.pack()
capitalise_checkbutton.pack()
capitalise_chance_title.pack()
capitalise_chance_inputfield.pack()
random_numbers_checkbutton.pack()
add_number_chance_title.pack()
add_number_chance_inputfield.pack()

# main program
words_list = words_file.words_list
# create passphrase with default settings when program is first loaded
create_passphrase(words_list,int(amount_of_words_inputfield.get()),should_space_words.get(),should_capitalise.get(),int(capitalise_chance_inputfield.get()), should_random_numbers.get(),int(add_number_chance_inputfield.get()))
# run gui loop
root.mainloop()

#changelog
# passphrase now copied to clipboard after generation
# capitalisiton is now random for each letter in a word rather than just the first letter of each word
# when 'capitalise letters' or 'generate number chance' is unselected their appropriate secondary option are disabled from being changed
# text of input fields are now centred