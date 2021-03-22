import random
import words_file
from tkinter import *

def main():
	# create the gui
	root = Tk()
	root.title("Passphrase generator")
	root.geometry("400x500")

	reg = root.register(callback) 

	amount_of_words_title = Label(root,text="Amount of words (1-20):")
	amount_of_words_inputfield = Entry(root,width=2)
	amount_of_words_inputfield.insert(0, 4)
	amount_of_words_inputfield.config(validate ="key",validatecommand =(reg, '%P', 20))

	should_space_words = IntVar()
	space_words_checkbutton = Checkbutton(root,text="Space between words",variable=should_space_words,width="20")
	space_words_checkbutton.select()

	should_capitalise = IntVar()
	capitalise_checkbutton = Checkbutton(root,text="capitalise letters",variable=should_capitalise,width="20",command=lambda: toggle_child_options(capitalise_chance_title,capitalise_chance_inputfield,should_capitalise.get()))
	capitalise_checkbutton.select()

	capitalise_chance_title = Label(root,text="Chance of each letter being capitalised:")
	capitalise_chance_inputfield = Entry(root,width="3",justify='center')
	capitalise_chance_inputfield.insert(0, 20)
	capitalise_chance_inputfield.config(validate ="key",validatecommand =(reg, '%P', 100))

	should_random_numbers = IntVar()
	random_numbers_checkbutton = Checkbutton(root,text="random numbers",variable=should_random_numbers,width="20",command=lambda: toggle_child_options(add_number_chance_title,add_number_chance_inputfield,should_random_numbers.get()))
	random_numbers_checkbutton.select()

	add_number_chance_title = Label(root,text="Add number chance:")
	add_number_chance_inputfield = Entry(root,width="3",justify='center')
	add_number_chance_inputfield.insert(0, 50)
	add_number_chance_inputfield.config(validate ="key",validatecommand =(reg, '%P', 100))

	generate_button = Button(root,text="Generate Passphrase",
	command=lambda: inputfield_validation(words_list,amount_of_words_inputfield.get(),should_space_words.get(),should_capitalise.get(),capitalise_chance_inputfield.get(),should_random_numbers.get(),add_number_chance_inputfield.get(),passphrase_text,root))

	passphrase_text = Entry(root,justify='center',width=40)

	show_passphrase = IntVar()
	show_passphrase_checkbutton = Checkbutton(root,text="Show passphrase",variable=show_passphrase,width="20",command=lambda: toggle_passphrase_visibility(passphrase_text,show_passphrase.get()))
	show_passphrase_checkbutton.select()

	passphrase_text.pack(pady=15)
	show_passphrase_checkbutton.pack()
	generate_button.pack(pady=10)
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

def inputfield_validation(words_list,amount_of_words,should_space_words,should_capitalise,capitalise_letter_chance,should_random_numbers,add_number_chance,passphrase_text,root):
	if (not amount_of_words):
		amount_of_words = 4
	elif not capitalise_letter_chance:
		capitalise_letter_chance = 20
	elif not add_number_chance:
		add_number_chance = 50
	else:
		# if all inputs are integers and meet requirements then generate passphrase
		print("word generated")
		create_passphrase(words_list,int(amount_of_words),should_space_words,should_capitalise,int(capitalise_letter_chance), should_random_numbers,int(add_number_chance),passphrase_text,root)

def create_passphrase(words_list,amount_of_words,should_space_words, should_capitalise, capitalise_letter_chance, should_random_numbers, add_number_chance,passphrase_text,root):
	# create list of random word codes
	word_codes = generate_word_codes(amount_of_words)

	# find words that match the generated word codes
	selected_words = find_selected_words(word_codes,words_list)

	# capitalise letters in words if desired
	if (should_capitalise):
		capitalise_selected_word(selected_words,capitalise_letter_chance/100)
	
	# generate random numbers to add to passphrase if desired
	if (should_random_numbers):
		numbers = generate_random_numbers_to_add(amount_of_words,add_number_chance)
	else:
		numbers=['' for i in range(amount_of_words)]	# fill with blank strings incase user does not want numbers

	if (should_space_words):
		space = ' '
	else:
		space = ''
	
	# create passphrase
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
		rolls = random.sample(range(1,6),5)	# generate list of 5 random dice rolls
		rolls_strings = [str(i) for i in rolls]	# convert integer list to string list 
		word_codes.append("".join(rolls_strings))	# add the rolls together to make a code and add to list
	return word_codes

def find_selected_words(word_codes,words_list):
	selected_words=[]
	for code in word_codes:
		# loop through each key in words_list to find matching word code
		if code in words_list.keys():
			selected_words.append(words_list[code])
		else:
			print("Problem occured with finding a word in list")
			quit()
	return selected_words

def capitalise_selected_word(selected_words,capitalise_letter_chance):
	for i, word in enumerate(selected_words):
			word_letters = list(word)	# create list of all characters in word

			for ii, letter in enumerate(word_letters):	# loop through all letters in word_letters
				if random.random() <= capitalise_letter_chance:	# check if random chance allows letter to be capitalised
					word_letters[ii] = letter.upper()
			
			# replace word with new letters
			selected_words[i] = "".join(word_letters)
	return selected_words

def generate_random_numbers_to_add(amount_of_words,add_number_chance):
	numbers=[]
	add_number_chance = add_number_chance/100
	for i in range(amount_of_words):
		if random.random() <= add_number_chance:
			numbers.append(str(random.SystemRandom().randint(1, 9)))			
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

# for validating what the user wants to input into an inputfield
def callback(input,max):
	if input.isdigit() and int(input) < int(max)+1 and input != '0': 
		return True
	elif input == "":
		return True
	else: 
		print("wanted to input: " + input)
		return False

if __name__ == "__main__":
	words_list = words_file.words_list	# import dictionary of words from other file
	main()

#changelog
# user cannot enter letters or values out of range into input fields.
# much faster way of randomly capitalising letters
# 30x faster capitalising words
# 7x faster generating word codes
# 3x faster generating random numbers