import nltk
import string
import math

"""Bayesian Classifier:
	Takes any spam message and decides if it's spam or not spam
	using the data gathered by spam_training"""

stop_words = [line.strip() for line in open('100_most_common.txt')]
master_dict = {}
spam_dict = {}
stop_words += list(string.punctuation)


def make_prob_dictionary(to_read, probabilities):
	"""Turn a text file of probabilities into a dictionary"""
	f = open(to_read)
	for i in f:
		x = i.strip().split()
		probabilities[x[0][:-1]] = float(x[1])
	f.close()
	return probabilities

def read_doc(item):
	"""Read an email and return the number of occurences and the word count"""
	words = 0
	directory = {}
	f = open(item)
	raw = f.read()
	for sent in nltk.sent_tokenize(raw.lower()):
	    for word in nltk.word_tokenize(sent):
	    	words += 1
	        try:
	            directory[word] = directory[word]+1
	        except KeyError:
	            directory[word] = 1
	return [directory, words]

def probabilities(doc, doc_length, prob_dict):
	"""See what the probability of a word occuring is in spam or ham"""
	for elem in doc:
		doc[elem] = doc[elem]/doc_length
	for key in doc.keys():
		if key in stop_words:
			doc.pop(key)
	for key in doc.keys():
		try:
			doc[key] = prob_dict[key]
		except KeyError:
			doc[key] = 0.0
			#doc[key] = doc[key]/doc_length
	return doc	

def classify_document(classification_file, classification_dict, document):
	"""Take a document and see how close it is spam or ham by its classification file."""
	document_dictionary = make_prob_dictionary(classification_file, classification_dict)
	document = read_doc(document)
	doc_words = document[0]
	doc_length = float(document[1])
	document = probabilities(doc_words, doc_length, classification_dict)
	return document

def main():
	doc = classify_document("ham.txt", master_dict, "testspam.text")
	spam_doc = classify_document("spam.txt", spam_dict, "testspam.text")

	if math.log(sum(spam_doc.values())/sum(doc.values())) > 0:
		print "Document is spam."
	else:
		print "Document is not spam."

if __name__ == '__main__':
	main()
