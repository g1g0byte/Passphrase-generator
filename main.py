import random, words_file
from tkinter import *

def main():
	# import dictionary of words from other file
	words_list = words_file.words_list
	
	# create the gui
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
	capitalise_checkbutton = Checkbutton(root,text="capitalise letters",variable=should_capitalise,width="20",command=lambda: toggle_child_options(capitalise_chance_title,capitalise_chance_inputfield,should_capitalise.get()))
	capitalise_checkbutton.select()

	capitalise_chance_title = Label(root,text="Chance of each letter being capitalised:")
	capitalise_chance_inputfield = Entry(root,width="3",justify='center')
	capitalise_chance_inputfield.insert(0, 20)

	should_random_numbers = IntVar()
	random_numbers_checkbutton = Checkbutton(root,text="random numbers",variable=should_random_numbers,width="20",command=lambda: toggle_child_options(add_number_chance_title,add_number_chance_inputfield,should_random_numbers.get()))
	random_numbers_checkbutton.select()

	add_number_chance_title = Label(root,text="Generate number chance:")
	add_number_chance_inputfield = Entry(root,width="3",justify='center')
	add_number_chance_inputfield.insert(0, 50)

	generate_button = Button(root,text="Generate Passphrase",
	command=lambda: create_passphrase(words_list,int(amount_of_words_inputfield.get()),should_space_words.get(),should_capitalise.get(),int(capitalise_chance_inputfield.get()),should_random_numbers.get(),int(add_number_chance_inputfield.get()),passphrase_text,root))

	passphrase_text = Entry(root,justify='center',width=40)

	show_passphrase = IntVar()
	show_passphrase_checkbutton = Checkbutton(root,text="Show passphrase",variable=show_passphrase,width="20",command=lambda: toggle_passphrase_visibility(passphrase_text,show_passphrase.get()))
	show_passphrase_checkbutton.select()

	passphrase_text.pack()
	show_passphrase_checkbutton.pack()
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
	
	# create passphrase with default settings when program is first loaded
	create_passphrase(words_list,int(amount_of_words_inputfield.get()),should_space_words.get(),should_capitalise.get(),int(capitalise_chance_inputfield.get()),should_random_numbers.get(),int(add_number_chance_inputfield.get()),passphrase_text,root)
	# run gui loop
	root.mainloop()

def create_passphrase(words_list,amount_of_words,should_space_words, should_capitalise, capitalise_letter_chance, should_random_numbers, add_number_chance,passphrase_text,root):
	# create list of random word codes
	word_codes = generate_word_codes(amount_of_words)

	# find words that match the generated word codes
	selected_words = find_selected_words(amount_of_words,word_codes,words_list)

	# capitalise letters in words if desired
	if (should_capitalise):
		capitalise_selected_word(amount_of_words,selected_words,capitalise_letter_chance)
	
	# generate random numbers to add to passphrase if desired
	if (should_random_numbers):
		numbers = generate_random_numbers_to_add(amount_of_words,add_number_chance)
	else:
		numbers=['' for i in range(amount_of_words)]	# fill with blank strings incase user does not want numbers

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

def generate_word_codes(amount_of_words):
	word_codes=[]
	for i in range(amount_of_words):
		word_code=''
		for i in range(5):
			word_code += str(random.SystemRandom().randint(1, 6))
		word_codes.append(word_code)
	return word_codes

def find_selected_words(amount_of_words,word_codes,words_list):
	selected_words=[]
	for i in range(amount_of_words):
		# loop through each key in words_list to find matching word code
		if word_codes[i] in words_list.keys():
			selected_words.append(words_list[word_codes[i]])
		else:
			print("Problem occured with finding a word in list")
			quit()
	return selected_words

def capitalise_selected_word(amount_of_words,selected_words,capitalise_letter_chance):
	for i in range(amount_of_words):
			for letter in selected_words[i]:
				chance = random.SystemRandom().randint(1, 100)
				if chance <= capitalise_letter_chance:
					selected_words[i] = selected_words[i].replace(letter,letter.upper())

def generate_random_numbers_to_add(amount_of_words,add_number_chance):
	numbers=[]
	for i in range(amount_of_words):
			chance = random.SystemRandom().randint(1, 100)
			if chance <= add_number_chance:
				numbers.append(str(random.SystemRandom().randint(1, 6)))
			else:
				numbers.append('')
	return numbers

def toggle_child_options(title,inputfield,enabled):
	if (not enabled):
		title.config(state='disabled')
		inputfield.config(state='disabled')
	else:
		title.config(state='normal')
		inputfield.config(state='normal')

def toggle_passphrase_visibility(text,enabled):
	if (not enabled):
		text.config(show='*')
	else:
		text.config(show='')

if __name__ == "__main__":
	main()

#changelog
# now run script trough if __name__ == "__main__" conditional
# made "toggle gui option" procedures into singular procedure
# code seperated into more functions
# ability to hide the passphrase 