import sys
import os
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

            words = Diff(result, stopWords)


    return result


def conditionalProbability(freq, uniqueWords, totalWordsInGroup):
    return ((freq + 1) + 1) / (uniqueWords + totalWordsInGroup)


def writeNModel(wordDetails):
    try:
        f = open("nModel.txt", "w+")
        f.write("%s: %s %s %s %s %s %s %s %s %s" % (
            'word', 'total', 'pos', 'neg', 'decep', 'truth', 'posProb', 'negProb', 'decepProb', 'truthProb'))
        f.write("\n")
        for word in wordDetails.keys():
            wordDetail = wordDetails[word]
            f.write("%s: %s %s %s %s %s %s %s %s %s" % (
                word, wordDetail['total'], wordDetail['positive'], wordDetail['negative'], wordDetail['deceptive'],
                wordDetail['truthful'], wordDetail['posProbability'], wordDetail['negProbability'],
                wordDetail['deceptiveProbability'], wordDetail['truthfulProbability']))
            f.write("\n")
    finally:
        f.close()


def

def readpath(inputPath):
    positiveWords = []
    negativeWords = []
    deceptiveWords = []
    truthfulWords = []

    positiveDeceptiveWords = Diff(dirWalk(positiveDeceptive), stopWords)
    positiveWords += positiveDeceptiveWords
    deceptiveWords += positiveDeceptiveWords
    # print positiveDeceptiveWords, len(positiveDeceptiveWords)

    positiveTruthfulWords = Diff(dirWalk(positiveTruthful), stopWords)
    positiveWords += positiveTruthfulWords
    truthfulWords += positiveTruthfulWords
    # print positiveTruthfulWords, len(positiveTruthfulWords)

    negativeDeceptiveWords = Diff(dirWalk(negativeDeceptive), stopWords)
    negativeWords += negativeDeceptiveWords
    deceptiveWords += negativeDeceptiveWords
    # print negativeDeceptiveWords, len(negativeDeceptiveWords)

    negativeTruthfulWords = Diff(dirWalk(negativeTruthful), stopWords)
    negativeWords += negativeTruthfulWords
    truthfulWords += negativeTruthfulWords
    # print negativeTruthfulWords, len(negativeTruthfulWords)

    # wordCount = Counter(positiveWords)
    # print(wordCount, Counter(positiveWords))
    # wordCount = wordCount + Counter(negativeWords)
    # print (wordCount)
    # print (len(wordCount))
    #
    # uniqueWords = set(wordCount.keys())
    # print (uniqueWords)
    # print (len(uniqueWords))

    positiveWordToCount = Counter(positiveWords)
    negativeWordCount = Counter(negativeWords)

    uniqueWordCount = positiveWordToCount + negativeWordCount

    deceptiveWordToCount = Counter(deceptiveWords)
    truthFulWordToCount = Counter(truthfulWords)

    wordDetails = {}

    for word in uniqueWordCount.keys():
        total = uniqueWordCount[word]
        positive = positiveWordToCount[word] if word in positiveWords else 0
        negative = negativeWordCount[word] if word in negativeWords else 0
        deceptive = deceptiveWordToCount[word] if word in deceptiveWords else 0
        truthful = truthFulWordToCount[word] if word in truthfulWords else 0

        wordDetails[word] = {'total': total,
                             'positive': positive,
                             'negative': negative,
                             'deceptive': deceptive,
                             'truthful': truthful,
                             'posProbability': findProbability(positive, len(uniqueWordCount), len(positiveWords)),
                             'negProbability': findProbability(negative, len(uniqueWordCount), len(negativeWords)),
                             'deceptiveProbability': findProbability(deceptive, len(uniqueWordCount),
                                                                     len(deceptiveWords)),
                             'truthfulProbability': findProbability(truthful, len(uniqueWordCount), len(truthfulWords))
                             }
    return wordDetails


if __name__ == "__main__":
    modelFile = "nbmodel.txt"
    inputPath = str(sys.argv[1])
    wordDetails = readpath(inputPath)
    writeNModel(wordDetails)
