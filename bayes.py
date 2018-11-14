# 1005031
# Arif Uz Zaman
# CSE,BUET

import math
import copy
import random
import operator
from timeit import default_timer as timer


testData = None
trainData = None

Tags = []
wordCount = {}
wordInClass = {}
trainVectors = {}
trainDocsInClass = {}

Words = []
ignore = ['',' ','-','a','an','the','to','it','this','at','as','in','is','are']


def fileInput():
	global trainData,testData

	with open("training.data","r+") as fhandle:
		Train = fhandle.read().replace("\n\n\n\n\n","\n\n\n").replace("\n\n\n\n","\n\n\n").lower()
		trainData = [[ topic for topic in article.split("\n\n")] for article in Train.split("\n\n\n")]

	with open("test.data","r+") as fhandle:
		Test = fhandle.read().replace("\n\n\n\n\n","\n\n\n").replace("\n\n\n\n","\n\n\n").lower()
		testData = [[ topic for topic in article.split("\n\n")] for article in Test.split("\n\n\n")]


def uniqueWord():
	global Words

	Words = set([])
	for x in xrange(len(trainData)):
		for y in xrange(1,len(trainData[x])):
			str1 = trainData[x][y].replace("\n"," ").replace("/"," ").replace(",","").replace("'s","").replace(".","").replace("+","")
			for word in str1.split(" "):
				if word in ignore:
					continue

				if word.isdigit():
					continue

				Words.add(word)

	Words = sorted(Words)


def featureVector(document):
	global Words
	vector = [ 0 for x in xrange(len(Words)) ]

	temp = {}
	for x in xrange(1,len(document)):
		str1 = document[x].replace("\n"," ").replace("/"," ").replace(",","").replace("'s","").replace(".","").replace("+","")
		for word in str1.split(" "):
			if word in ignore:
				continue

			if word.isdigit():
				continue

			if word in temp:
				temp[word] += 1
			else:
				temp[word] = 1

	for key in temp:
		indx = Words.index(key)
		vector[indx] = temp[key]

	return vector


def classStatistics():
	global trainDocsInClass,wordInClass,Tags

	temp = set([])
	for x in xrange(len(trainData)):
		v1 = trainVectors[x]
		tag = trainData[x][0]
		temp.add(tag)

		if tag in trainDocsInClass:
			trainDocsInClass[tag] += 1
		else:
			trainDocsInClass[tag] = 1

		if tag in wordInClass:
			wordInClass[tag] += sum(v1)
		else:
			wordInClass[tag] = sum(v1)

	Tags = sorted(temp)


def wordFrequency():
	global wordCount

	temp = [ 0 for x in xrange(len(Tags)) ]
	for x in xrange(len(Words)):
		wordCount[x] = temp

	for x in xrange(len(trainData)):
		tag = trainData[x][0]
		v1 = trainVectors[x]
		indx = Tags.index(tag)

		for x in xrange(len(Words)):
			temp = copy.deepcopy(wordCount[x])
			temp[indx] += v1[x]
			wordCount[x] = temp


def pWord(word,tag,factor):
	indx = Tags.index(tag)

	if word in Words:
		key = Words.index(word)
		value1 = wordCount[key][indx]
	else:
		value1 = 0

	value2 = wordInClass[tag]

	return math.log10((factor+value1)/float(len(Words)+value2))


def pWClass(document,tag):
	pW = 0
	for x in xrange(1,len(document)):
		str1 = document[x].replace("\n"," ").replace("/"," ").replace(",","").replace("'s","").replace(".","").replace("+","")
		for word in str1.split(" "):
			if word in ignore:
				continue

			if word.isdigit():
				continue

			pW += pWord(word,tag,2)

	return pW


def findClass():
	results = []
	for x in xrange(len(testData)):
		temp = {}

		for key in trainDocsInClass:
			pC = trainDocsInClass[key]/float(len(trainData))
			temp[key] = pWClass(testData[x],key) + math.log10(pC)

		sorted_temp = sorted(temp.iteritems(), key=operator.itemgetter(1), reverse=True)
		tag = sorted_temp[0][0]
		results.append(tag)

	return results


def testFindings():
	taglist = findClass()

	count = 0
	for x in xrange(len(taglist)):
		if testData[x][0] == taglist[x]:
			count += 1

	print
	print ("Accuracy : %3.1f") % (count/float(len(testData)) * 100)


def main():
	global trainData,testData,trainVectors
	print "Running Naive Bayes Algorithm..."

	fileInput()
	random.shuffle(trainData)
	random.shuffle(testData)
	trainData,testData = trainData[:100],testData[:100]
	uniqueWord()

	for x in xrange(len(trainData)):
		trainVectors[x] = featureVector(trainData[x])

	classStatistics()
	wordFrequency()
	testFindings()


if __name__ == '__main__':
	random.seed(1000)
	start = timer()
	main()
	end = timer()

	print
	print ("Program Run Time = %3.2f min") % ((end - start)/60)