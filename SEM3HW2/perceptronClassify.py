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

def getLearnedWords(path):
    wordsLearn = {}
    with open(path, 'r') as f:
        data = f.read().splitlines()

    numberOfWords = data.pop(0)
    wordName, count = numberOfWords.split()[0], numberOfWords.split()[1]

    for i in range(0, int(count)):
        values = data.pop(0).split()
        print values
        wordsLearn[values[0]] = values[1]

    b1andb2Count = data.pop(0).split()
    b1andb2Value = data.pop(0).split()
    b1 = b1andb2Value[0]
    b2 = b1andb2Value[1]

    return wordsLearn, b1, b2

def classify(inputPath, wordsLearned, b1, b2):
    words = wordsLearned.keys()
    positive = inputPath + 'positive_polarity/'
    negative = inputPath + 'negative_polarity/'
    positiveDeceptive = positive + 'deceptive_from_MTurk/'
    positiveTruthful = positive + 'truthful_from_Web/'
    negativeDeceptive = negative + 'deceptive_from_MTurk/'
    negativeTruthful = negative + 'truthful_from_Web/'
    allPaths = []

    allPaths += getFilePaths(positiveDeceptive)
    allPaths += getFilePaths(positiveTruthful)
    allPaths += getFilePaths(negativeDeceptive)
    allPaths += getFilePaths(negativeTruthful)

    output = []
    for filePath in allPaths:
        fileWords = set(extractWords(filePath))
        a1 = 0
        a2 = 0

        for word in fileWords:
            if word in words:
                a1 += int(wordsLearned[word]) * 1 + int(b1)
                a2 += int(wordsLearned[word]) * 1 + int(b2)

        posOrNeg = 'POSITIVE' if a1 > 0 else 'NEGATIVE'
        decOrTru = 'TRUTHFUL' if a1 > 0 else 'DECEPTIVE'
        output.append([filePath, posOrNeg, decOrTru])

    with open("perceptronClassify.txt", "w+") as f:
        for valueArray in output:
            f.write("%s %s %s" % (valueArray[0], valueArray[1], valueArray[2]))
            f.write("\n")

if __name__ == "__main__":
    learnFilePath = str(sys.argv[1])
    inputPath = str(sys.argv[2])
    wordsLearned, b1, b2 = getLearnedWords(learnFilePath)
    classify(inputPath, wordsLearned, b1, b2)