import argparse
import sys
import collections

parser = argparse.ArgumentParser(
    description='Calculate firs applicant to be selected')
parser.add_argument('-i', '--input',
                    help='Input File', type=str, required=True)
args = vars(parser.parse_args(sys.argv[1:]))
inputFile = args['input']

data = None
with open(inputFile, 'r') as f:
    data = f.read().splitlines()

# Common method for getting list of already assigned applicants
def getAllotedIds(data, allotedIds):
    for i in range(noOfBedsAlloted):
        allotedIds.append(data.pop(0))


def binaryNumberForAllotedIds(total, binaryArray):
    binaryString = ''
    for x in binaryArray:
        if x >= total:
            binaryString += '1'
        else:
            binaryString += '0'
    return binaryString


# total beds and spaces
totalBeds = int(data.pop(0))
totalSpaces = int(data.pop(0))

# Already alloted beds + applicant ids
noOfBedsAlloted = int(data.pop(0))
selectedLHSAIds = []
getAllotedIds(data, selectedLHSAIds)

# Already alloted spaces + applicant ids
noOfSpacesAlloted = int(data.pop(0))
selectedSPLAIds = []
getAllotedIds(data, selectedSPLAIds)

# total applicants
totalApplicants = int(data.pop(0))

idToWeekMap = {}
lhsaApplicantIds = []
splaApplicantIds = []
lhsaBinaryArray = [0] * 7
splaBinariesArray = [0] * 7

for i in range(totalApplicants):
    applicant = data.pop(0)
    id = applicant[:5]

    gender = applicant[5]
    age = int(applicant[6:9])
    pets = applicant[9]
    medical = applicant[10]
    car = applicant[11]
    carLicense = applicant[12]
    week = applicant[-7:]

    if (selectedLHSAIds.__contains__(id)):
        for index, item in enumerate(week):
            lhsaBinaryArray[index] += int(item)
        continue

    if (selectedSPLAIds.__contains__(id)):
        for index, item in enumerate(week):
            splaBinariesArray[index] += int(item)
        continue

    # Get LHSA matching applicants
    if gender == 'F' and age > 17 and pets == 'N':
        lhsaApplicantIds.append(id)
        idToWeekMap[id] = week

    # Get SPLA matching applicants
    if car == 'Y' and carLicense == 'Y' and medical == 'N':
        splaApplicantIds.append(id)
        idToWeekMap[id] = week

# Get already alloted applicants for the next week in binary
lhsaBinary = binaryNumberForAllotedIds(totalBeds, lhsaBinaryArray)
splaBinary = binaryNumberForAllotedIds(totalSpaces, splaBinariesArray)

matchingApplicants = []

#If all LHSA beds are already full do not check for intersection
if lhsaBinary.count('1') != 7:
    matchingApplicants = list(set(lhsaApplicantIds) & set(splaApplicantIds))


max = 0
outputId = None
for applicantId in splaApplicantIds:
    weekBinary = idToWeekMap[applicantId]

    xorResult = '{0:0{1}b}'.format(int(splaBinary, 2) ^ int(weekBinary, 2), len(weekBinary))
    andResult = '{0:0{1}b}'.format(int(xorResult, 2) & int(weekBinary, 2), len(weekBinary))

    count = andResult.count('1')
    if count > max:
        max = count
        outputId = applicantId

print outputId
