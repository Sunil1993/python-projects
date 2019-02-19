import sys
import os

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

def getFilePaths(fileRoot):
    paths = []
    for root, dirs, files in os.walk(fileRoot, topdown=True):
        files = [f for f in files if not f[0] == '.']
        for f in files:
            paths.append(os.path.join(root, f))

    return paths

def loadVocabulary():
    vocabulary = {}
    data = None
    with open(os.path.join(os.path.dirname(__file__), 'vocabulary.txt'), 'r') as f:
        data = f.read().splitlines()

    for line in data:
        vocabLine = line.split()
        vocabulary[vocabLine[0]] = vocabLine[1]

    return vocabulary

def selectFilePath(posDecPaths, posTruPaths, negDecPaths, negTruPaths, index):
    if index == 0 and len(posDecPaths) > 0:
        return 1, -1, posDecPaths.pop()
    elif index == 1 and len(negDecPaths) > 0:
        return -1, -1, negDecPaths.pop()
    elif index == 2 and len(posTruPaths) > 0:
        return 1, 1, posTruPaths.pop()
    elif index == 3 and len(negTruPaths) > 0:
        return -1, 1, negTruPaths.pop()
    else:
        return selectFilePath(posDecPaths, posTruPaths, negDecPaths, negTruPaths, (index + 1) % 4)

def calculatePerceptron(vocabulary, inputPath):
    vocabularyWords = vocabulary.keys()
    vocabularyCount = len(vocabularyWords)
    positive = inputPath + 'positive_polarity/'
    negative = inputPath + 'negative_polarity/'
    positiveDeceptive = positive + 'deceptive_from_MTurk/'
    positiveTruthful = positive + 'truthful_from_Web/'
    negativeDeceptive = negative + 'deceptive_from_MTurk/'
    negativeTruthful = negative + 'truthful_from_Web/'
    w = [0] * vocabularyCount
    b1 = 0
    b2 = 0

    posDeceptiveFilePaths = getFilePaths(positiveDeceptive)
    posTruthFulFilePaths = getFilePaths(positiveTruthful)
    negDeceptiveFilePaths = getFilePaths(negativeDeceptive)
    negTruthfulFilePaths = getFilePaths(negativeTruthful)

    positivePaths = posDeceptiveFilePaths + posTruthFulFilePaths
    negativePaths = negDeceptiveFilePaths + negTruthfulFilePaths
    allPaths = positivePaths + negativePaths

    for it in range(0, 1):
        tempPosDecPaths = [] + posDeceptiveFilePaths
        tempPosTruPaths = [] + posTruthFulFilePaths
        tempNegDecPaths = [] + negDeceptiveFilePaths
        tempNegTruPaths = [] + negTruthfulFilePaths
        for fileCount in range(0, len(allPaths)):
            y1, y2, filePath = selectFilePath(tempPosDecPaths, tempPosTruPaths, tempNegDecPaths, tempNegTruPaths, fileCount % 4)

            fileWords = set(extractWords(filePath))
            a1 = 0
            a2 = 0

            for element in fileWords:
                if element in vocabularyWords:
                    vIndex = vocabularyWords.index(element)
                    a1 += w[vIndex] * 1 + b1
                    a2 += w[vIndex] * 1 + b2

            if (a1 * y1) <= 0:
                for element in fileWords:
                    if element in vocabularyWords:
                        vIndex = vocabularyWords.index(element)
                        w[vIndex] += y1 * 1
                b1 += y1

            if (a2 * y2) <= 0:
                for element in fileWords:
                    if element in vocabularyWords:
                        vIndex = vocabularyWords.index(element)
                        w[vIndex] += y2 * 1
                b2 += y2

    with open("perceptron.txt", "w+") as f:
        f.write("%s %s" % ("percentron_words", vocabularyCount))
        for index in range(0, vocabularyCount):
            f.write("\n")
            f.write("%s %s" % (vocabularyWords[index], w[index]))

        f.write("\n")
        f.write("%s %s" % ("b1b2", "1"))
        f.write("\n")
        f.write("%s %s" % (b1, b2))



if __name__ == "__main__":
    vocabulary = loadVocabulary()
    inputPath = str(sys.argv[1])
    calculatePerceptron(vocabulary, inputPath)