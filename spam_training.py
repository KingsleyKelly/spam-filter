import os
import nltk
import random
import string



""" Training for Bayes Classifier for Spam Detection.
	Reads in all emails in folders contained in ham_emails and spam_emails.
	Uses nltk to determine which are the most common words and prints a
	text file with the percentages with which words occur. 

	Performs 10-fold cross validation on the data, and removes the 100 most
	common english words and punctuation from the training set.
	"""

def add_directories(directory, directory2):
	"""Add the values of two directories"""
	for elem in directory:
		try:
			directory[elem] = directory.get(elem,0) + (directory2[elem])
		except KeyError:
			directory[elem] = directory[elem]
	return directory


def count_to_frequency(directory, word_count):
	"""Convert word count to frequency of appearance in text"""
	for elem in directory:
		directory[elem] = directory[elem]/word_count
	return directory


def get_directory_freq(mail, directory):
	"""Work out the occurences of words in a given directory"""
	words = 0
	cross_fold = (os.listdir(mail))
	random.shuffle(cross_fold)
	cross_fold = cross_fold[:len(cross_fold)/2]

	for item in cross_fold:
		
		f = open(mail+item)
		raw = f.read()
		for sent in nltk.sent_tokenize(raw.lower()):

		    for word in nltk.word_tokenize(sent):
		    	words += 1
		        try:
		            directory[word] = directory[word]+1
		        except KeyError:
		            directory[word] = 1

	return [directory, float(words)]


def print_directory(text,directory):
	"""Print out a directory as oredered key, values"""
	f = open(text, 'w')
	for key, value in reversed(sorted(directory.iteritems(), key=lambda (k,v): (v,k))):

		x = "%s: %s\n" % (key, value)
		f.write(x)
	f.close()


def email_training(emails, directory):
	"""Builds a training set from the given emails and adds it to to the final collection of emails"""
	word_count = 0
	for email in emails:
		email_return = get_directory_freq(email, directory)
		temp_directory = email_return[0]
		word_count += email_return[1]
		directory = add_directories(directory, temp_directory)
	stop_words = [line.strip() for line in open('100_most_common.txt')]
	stop_words += list(string.punctuation)
	for key in directory.keys():
		if key in stop_words:
			directory.pop(key)
	directory = count_to_frequency(temp_directory, word_count)
	return directory

def main():

	ham_directory = {}
	spam_directory = {}
	for i in range(10):
		#10 fold cross-validation
		ham_emails = ['easy_ham/', 'easy_ham_2/', 'hard_ham/', 'hard_ham_2/']
		spam_emails = ['spam/', 'spam_2/']
		ham_directory = email_training(ham_emails, ham_directory)
		spam_directory = email_training(spam_emails, spam_directory)

	print_directory("ham.txt", ham_directory)
	print_directory("spam.txt", spam_directory)

if __name__ == '__main__':
	main()


