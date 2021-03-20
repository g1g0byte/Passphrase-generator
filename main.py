import csv,random

def read_words_file():
	words_list = {}
	with open('words.csv', 'r') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			words_list.update({row[0]:row[1]})
	return words_list

def amount_of_words_input():
	while True:
		try:
			amount_of_words = int(input("Enter amount of words to use: "))
			if amount_of_words <= 0 or amount_of_words > 100:
				print("Please enter a reasonable amount of words! (0 < amount <= 100)\n")
				continue
		
		except ValueError:# Handle if input is not an integer
			print("Please enter an amount of words!\n")
			continue
		else:
			return amount_of_words

def should_space_words_input():
	while True:
		try:
			should_space_words = int(input("Do you want spaces between words? (yes=1,no=0) : "))
			if should_space_words not in [1,0]:
				print("Please enter 1 (yes) or 0 (no)!\n")
				continue

		except ValueError:	# Handle if input is not an integer
			print("Please enter 1 (yes) or 0 (no)!\n")
			continue
		
		if should_space_words == 1:
			return True
		else:
			return False

def should_random_numbers_input():
	while True:
		try:
			should_random_numbers = int(input("Do you want a random number at end of each word? (yes=1,no=0) : "))
			if should_random_numbers not in [1,0]:
				print("Please enter 1 (yes) or 0 (no)!\n")
				continue

		except ValueError:	# Handle if input is not an integer
			print("Please enter 1 (yes) or 0 (no)!\n")
			continue
		
		if should_random_numbers == 1:
			return True
		else:
			return False

def should_capitalise_input():
	while True:
		try:
			should_capitalise = int(input("Do you want to capitalise the first letter of each word? (yes=1,no=0) : "))
			if should_capitalise not in [1,0]:
				print("Please enter 1 (yes) or 0 (no)!\n")
				continue

		except ValueError:	# Handle if input is not an integer
			print("Please enter 1 (yes) or 0 (no)!\n")
			continue
		
		if should_capitalise == 1:
			return True
		else:
			return False

def generate_word_codes(amount_of_words):
	word_codes=[]
	for i in range(amount_of_words):
		word_code=''
		for i in range(5):
			roll = random.SystemRandom().randint(1, 6)
			word_code += str(roll)
		word_codes.append(word_code)
	return word_codes

def find_words_list(words_list,word_codes):
	selected_words=[]
	for i in range(len(word_codes)):
		if word_codes[i] in words_list.keys():
			selected_words.append(words_list[word_codes[i]])
		else:
			print("Problem occured with finding word in list")
			quit()
	return selected_words

def create_passphrase(selected_words, should_space_words, should_capitalise, should_random_numbers):
	amount_of_words = len(selected_words)
	if (should_capitalise):
		for i in range(amount_of_words):
			selected_words[i] = selected_words[i].capitalize()
	
	numbers=['' for i in range(amount_of_words)]
	add_number_chance = 50
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
		passphrase = passphrase+selected_words[i]+numbers[i]+space
	return passphrase

# main program
words_list = read_words_file()
#-------------------------------------------------
amount_of_words = amount_of_words_input()
should_space_words = should_space_words_input()
should_capitalise = should_capitalise_input()
should_random_numbers = should_random_numbers_input()
#-------------------------------------------------
word_codes = generate_word_codes(amount_of_words)
selected_words = find_words_list(words_list, word_codes)
print(word_codes)
print(selected_words)
#-------------------------------------------------
passphrase = create_passphrase(selected_words, should_space_words, should_capitalise, should_random_numbers)
print(passphrase)