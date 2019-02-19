import sys
import os
from collections import Counter

stopWords = ["a", "im", "am", "an", "and", "at", "be", "by", "can", "could", "did", "do", "from", "for", "have",
             "had", "has", "he", "her", "hers", "his", "is", "in", "i", "it", "its", "me", "mine", "my", "on",
             "of", "our", "she", "so", "that", "the", "to", "then", "them", "this", "those", "us", "we", "was",
             "were", "will", "with", "where", "were", "would", "you", "your"]


def Diff(li1, li2):
    return [item for item in li1  if item not in li2]


def extractWords(filePath):
    fileContent = None
    with open(filePath) as fp:
        fileContent = fp.read().replace('\n', ' ').lower()
    # return filter(None, map(lambda word: ''.join(filter(str.isalnum(), word)), fileContent.split()))
    return filter(None, Diff(map(lambda word: ''.join(filter(str.isalpha, word)), fileContent.split()), stopWords))


def dirWalk(fileRoot):
    result = []
    for root, dirs, files in os.walk(fileRoot, topdown=True):
        files = [f for f in files if not f[0] == '.']
        for f in files:
            result += extractWords(os.path.join(root, f))
    return result

def writeVocabularyToFile(wordTuples):
    with open("vocabulary.txt", "w+") as f:
        for wordTuple in wordTuples:
            f.write("%s %s" % (wordTuple[0], wordTuple[1]))
            f.write("\n")

def readPath(inputPath):
    positive = inputPath + 'positive_polarity/'
    negative = inputPath + 'negative_polarity/'
    positiveDeceptive = positive + 'deceptive_from_MTurk/'
    positiveTruthful = positive + 'truthful_from_Web/'
    negativeDeceptive = negative + 'deceptive_from_MTurk/'
    negativeTruthful = negative + 'truthful_from_Web/'
    positiveWords = []
    negativeWords = []

    positiveDeceptiveWords = dirWalk(positiveDeceptive)
    positiveWords += positiveDeceptiveWords

    positiveTruthfulWords = dirWalk(positiveTruthful)
    positiveWords += positiveTruthfulWords

    negativeDeceptiveWords = dirWalk(negativeDeceptive)
    negativeWords += negativeDeceptiveWords


    negativeTruthfulWords = dirWalk(negativeTruthful)
    negativeWords += negativeTruthfulWords

    uniqueWords = positiveWords  + negativeWords

    return Counter(uniqueWords).most_common(1000)

if __name__ == "__main__":
    inputPath = str(sys.argv[1])
    wordTuples = readPath(inputPath)
    writeVocabularyToFile(wordTuples)
