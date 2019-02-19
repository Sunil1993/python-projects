import sys
import os
import math
from collections import Counter

stopWords = ["a", "im", "am", "an", "and", "at", "be", "by", "can", "could", "did", "do", "from", "for", "have",
             "had", "has", "he", "her", "hers", "his", "is", "in", "i", "it", "its", "me", "mine", "my", "on",
             "of", "our", "she", "so", "that", "the", "to", "then", "them", "this", "those", "us", "we", "was",
             "were", "will", "with", "where", "were", "would", "you", "your"]


def Diff(li1, li2):
    return (list(set(li1) - set(li2)))


def extractWords(filePath):
    fileContent = None
    with open(filePath) as fp:
        fileContent = fp.read().replace('\n', ' ').lower()
    # return filter(None, map(lambda word: ''.join(filter(str.isalnum(), word)), fileContent.split()))
    return filter(None, map(lambda word: ''.join(filter(str.isalpha, word)), fileContent.split()))


def dirWalk(fileRoot):
    result = []
    for root, dirs, files in os.walk(fileRoot, topdown=True):
        files = [f for f in files if not f[0] == '.']
        for f in files:
            result += extractWords(os.path.join(root, f))
    return result


def extractDataFromFile():
    with open(os.path.join(os.path.dirname(__file__), 'nModel.txt'), 'r') as f:
        data = f.read().splitlines()

    probabilityLine = data.pop(0).split()
    priorProbabilities = {
        'priorPos': float(probabilityLine[0]),
        'priorNeg': float(probabilityLine[1]),
        'priorDec': float(probabilityLine[2]),
        'priorTru': float(probabilityLine[3])
    }

    wordDetails = {}
    for line in data:
        wordLine = line.split()
        wordDetails[wordLine[0]] = {'total': float(wordLine[1]),
                                    'positive': float(wordLine[2]),
                                    'negative': float(wordLine[3]),
                                    'deceptive': float(wordLine[4]),
                                    'truthful': float(wordLine[5]),
                                    'posProbability': float(wordLine[6]),
                                    'negProbability': float(wordLine[7]),
                                    'deceptiveProbability': float(wordLine[8]),
                                    'truthfulProbability': float(wordLine[9])
                                    }

    return wordDetails, priorProbabilities


def nbclassify(fileRoot, wordDetails, priorProbabilities):
    with open("nbClassify.txt", "w+") as writef:
        for root, dirs, files in os.walk(fileRoot, topdown=True):
            files = [f for f in files if not f[0] == '.']
            for f in files:
                totalPos = 0
                totalNeg = 0
                totalTru = 0
                totalDec = 0
                result = extractWords(os.path.join(root, f))

                words = Diff(result, stopWords)
                for word in words:
                    if (word in wordDetails.keys()):
                        totalPos += math.log10(wordDetails[word]['posProbability']) + math.log10(
                            priorProbabilities['priorPos'])
                        totalNeg += math.log10(wordDetails[word]['negProbability']) + math.log10(
                            priorProbabilities['priorNeg'])
                        totalDec += math.log10(wordDetails[word]['deceptiveProbability']) + math.log10(
                            priorProbabilities['priorDec'])
                        totalTru += math.log10(wordDetails[word]['truthfulProbability']) + math.log10(
                            priorProbabilities['priorTru'])

                posNegVal = "POSITIVE" if totalPos >= totalNeg else "NEGATIVE"
                decTrueVal = "DECEPTIVE" if totalDec >= totalTru else "TRUTHFUL"
                writef.write("%s %s %s" % (os.path.join(root, f), posNegVal, decTrueVal))
                writef.write("\n")


if __name__ == "__main__":
    wordDetails, priorProbabilities = extractDataFromFile()

    # modelFile = "nbmodel.txt"
    # inputPath = str(sys.argv[1])
    # wordDetails, priorProbabilities = readpath(inputPath)
    # # writeNModel(wordDetails)
    nbClassifyFilesPath = str(sys.argv[1])
    nbclassify(nbClassifyFilesPath, wordDetails, priorProbabilities)
