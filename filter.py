import re
from collections import defaultdict
from math import log
from functools import reduce


# with open('./stopwords/stopwords.txt', 'r') as stop1:
# 	stopwords1 = stop1.read().strip().split('\n')
# with open('./stopwords/stopwords2.txt', 'r') as stop2:
# 	stopwords2 = stop2.read().strip().split('\n')
# stopwords = stopwords1 + list(set(stopwords2) - set(stopwords1))

# with open('train.txt') as trainingData:
# 	hamWords = defaultdict(int)
# 	spamWords = defaultdict(int)
# 	totalHam = 0
# 	totalSpam = 0

# 	for filePath in trainingData:
# 		fullPath = ('./ham/' + filePath if 'ham' in filePath else './spam/' + filePath).strip()
# 		with open(fullPath, encoding='utf-8', errors='ignore') as trainingFile:
# 			text = trainingFile.read().strip()

# 			words = re.split('\W+', text)
# 			words = [word.lower() for word in words if word not in stopwords]
			
# 			for word in words:
# 				if 'ham' in filePath:
# 					hamWords[word] += 1
# 					totalHam += 1
# 				else:
# 					spamWords[word] += 1
# 					totalSpam += 1

def naive(spamWords, hamWords, stopwords, totalHam, totalSpam):
	with open('naive-output.out', 'w+') as outputFile:
		countBadGuesses = 0
		countTotalFiles = 0
		with open('test.txt') as testData:
			for filePath in testData:
				fullPath = ('./ham/' + filePath if 'ham' in filePath else './spam/' + filePath).strip()
				label = 'ham' if 'ham' in filePath else 'spam'
				
				with open(fullPath, encoding='utf-8', errors='ignore') as testFile:
					text = testFile.read().strip()

					words = re.split('\W+', text)
					words = [word.lower() for word in words if word not in stopwords]

				# P(w_k | spam) / P(w_k | ham) for each word
				# itt lehet nem totalSpam es totalHam-mel kell osztani hanem (count(hamWords) + count(spamWords))
				# probability = sum([ (log(spamWords[w]) - log(totalSpam)) - (log(hamWords[w]) - log(totalHam)) for w in words if spamWords[w] > 0 and hamWords[w] > 0 ])

				tmp = ( totalHam / (totalHam + totalSpam) ) / ( 1 - totalHam / (totalHam + totalSpam))  
				probability = reduce(lambda x, y: x*y, [ (hamWords[w] / totalHam) / (spamWords[w] / totalSpam) * tmp for w in words if spamWords[w] > 0 and hamWords[w] > 0 ])
				
				# probability = reduce(lambda x, y: x*y, [ (hamWords[w] / totalHam) / (spamWords[w] / totalSpam) for w in words if spamWords[w] > 0 and hamWords[w] > 0 ])

				if probability < 1:
					guess = 'spam'
				else:
					guess = 'ham'
				
				if label != guess:
					countBadGuesses += 1
				countTotalFiles += 1
				outputFile.write(label + ' ' + guess + '\n')

		outputFile.write(str(countBadGuesses / countTotalFiles))


def smoothed(spamWords, hamWords, stopwords, alpha):
	with open('smoothed-output.out', 'w+') as outputFile:
		countBadGuesses = 0
		countTotalFiles = 0
		with open('test.txt') as testData:
			for filePath in testData:
				fullPath = ('./ham/' + filePath if 'ham' in filePath else './spam/' + filePath).strip()
				label = 'ham' if 'ham' in filePath else 'spam'
				
				with open(fullPath, encoding='utf-8', errors='ignore') as testFile:
					text = testFile.read().strip()

					words = re.split('\W+', text)
					words = [word.lower() for word in words if word not in stopwords]

				# P(w_k | spam) / P(w_k | ham) for each word
				# itt lehet nem totalSpam es totalHam-mel kell osztani hanem (count(hamWords) + count(spamWords))

				tmp = ( totalHam / (totalHam + totalSpam) ) / ( 1 - totalHam / (totalHam + totalSpam))  
				probability = reduce(lambda x, y: x*y, [ ((hamWords[w] + alpha) / (totalHam * 1 + alpha)) / (spamWords[w] / totalSpam) * tmp for w in words if spamWords[w] > 0 and hamWords[w] > 0 ])
				
				
				if probability < 1:
					guess = 'spam'
				else:
					guess = 'ham'
				
				if label != guess:
					countBadGuesses += 1
				countTotalFiles += 1
				outputFile.write(label + ' ' + guess + '\n')

		outputFile.write(str(countBadGuesses / countTotalFiles))


def crossValidate(trainingFilenames, n):
	parameterOptions = [1, 2, 3, 5, 7]
	groups = ['' for i in range(n)]
	trainingFileLines = trainingFileContents.split('\n')
	for i in range(len(trainingFileLines)):
		groups[i % n] += trainingFileLines[i] + '\n'
	
	avgErrors = []
	for h in range(len(parameterOptions)):
		testErrors = []
		for i in range(n):
			testErrors.append(knnReturningTestError(''.join([groups[j] for j in range(n) if j != i]), groups[i], parameterOptions[h]))
		avgErrors.append(sum(testErrors) / len(testErrors))
	return parameterOptions[avgErrors.index(min(avgErrors))]



if __name__ == "__main__":
	# merge stopwords
	with open('./stopwords/stopwords.txt', 'r') as stop1:
		stopwords1 = stop1.read().strip().split('\n')
	with open('./stopwords/stopwords2.txt', 'r') as stop2:
		stopwords2 = stop2.read().strip().split('\n')
	stopwords = stopwords1 + list(set(stopwords2) - set(stopwords1))
	
	with open('train.txt') as trainingData:
		hamWordCounts = defaultdict(int)
		spamWordCounts = defaultdict(int)
		totalHam = 0
		totalSpam = 0

		for filePath in trainingData:
			fullPath = ('./ham/' + filePath if 'ham' in filePath else './spam/' + filePath).strip()
			with open(fullPath, encoding='utf-8', errors='ignore') as trainingFile:
				text = trainingFile.read().strip()

				words = re.split('\W+', text)
				words = [word.lower() for word in words if word not in stopwords]
				
				for word in words:
					if 'ham' in filePath:
						hamWordCounts[word] += 1
						totalHam += 1
					else:
						spamWordCounts[word] += 1
						totalSpam += 1
	
	# naive(spamWordCounts, hamWordCounts, stopwords, totalHam, totalSpam)

	bestAlpha = crossValidate(, 5)
	smoothed(spamWordCounts, hamWordCounts, stopwords, 0.5)