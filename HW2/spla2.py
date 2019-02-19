import argparse
import sys

parser = argparse.ArgumentParser(
    description='Calculate first applicant to be selected')
parser.add_argument('-i', '--input',
                    help='Input File', type=str, required=True)
args = vars(parser.parse_args(sys.argv[1:]))
inputFile = args['input']

# Read file line by line
data = None
with open(inputFile, 'r') as f:
    data = f.read().splitlines()


# Common method for getting list of already assigned applicants
def get_alloted_ids(data, allotedIds, allotedNumber):
    for i in range(allotedNumber):
        allotedIds.append(data.pop(0))


# Get already allotted applicants for the next week in binary
def binary_number_for_alloted_ids(total, binaryArray):
    result = list(map(lambda x: '1' if x == total else '0', binaryArray))
    return ''.join(map(str, result))


# Calculate the first applicant from set of applicants
def calculate_spla_applicant(data):
    idToWeekMap = {}
    lhsaApplicantIds = []
    splaApplicantIds = []

    # array binary which represents next 7 days allotment
    lhsaFilledSpaces = [0] * 7
    splaFilledSpaces = [0] * 7

    totalBeds = int(data.pop(0))
    totalSpaces = int(data.pop(0))

    # Already allotted beds + applicant ids
    noOfBedsAlloted = int(data.pop(0))
    selectedLHSAIds = []
    get_alloted_ids(data, selectedLHSAIds, noOfBedsAlloted)

    # Already allotted spaces + applicant ids
    noOfSpacesAlloted = int(data.pop(0))
    selectedSPLAIds = []
    get_alloted_ids(data, selectedSPLAIds, noOfSpacesAlloted)

    # total applicants
    totalApplicants = int(data.pop(0))

    finalSplaMax = 0
    finalLhsaMax = 0

    def get_applicant_id_to_week_mapping(data):
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
                    lhsaFilledSpaces[index] += int(item)
                continue

            if (selectedSPLAIds.__contains__(id)):
                for index, item in enumerate(week):
                    splaFilledSpaces[index] += int(item)
                continue

            # Get LHSA matching applicants
            if gender == 'F' and age > 17 and pets == 'N':
                lhsaApplicantIds.append(id)
                idToWeekMap[id] = week

            # Get SPLA matching applicants
            if car == 'Y' and carLicense == 'Y' and medical == 'N':
                splaApplicantIds.append(id)
                idToWeekMap[id] = week

    def get_best_applicant_from_list(applicantIdArray, maxCount, selectedId, splaBinary):
        applicantIdArray.sort()
        for applicantId in applicantIdArray:
            weekBinary = idToWeekMap[applicantId]

            xorResult = '{0:0{1}b}'.format(int(splaBinary, 2) ^ int(weekBinary, 2), len(weekBinary))
            andResult = '{0:0{1}b}'.format(int(xorResult, 2) & int(weekBinary, 2), len(weekBinary))

            count = andResult.count('1')
            if count > maxCount:
                maxCount = count
                selectedId = applicantId

        return selectedId

    def calculateDaysForAppliantId(applicantId, occupiedSeats, isSpla):
        totalNumber = (lambda: totalSpaces, lambda: totalBeds)[isSpla]()
        binaryNumber = binary_number_for_alloted_ids(totalNumber, occupiedSeats)

        weekBinary = idToWeekMap[applicantId]

        xorResult = '{0:0{1}b}'.format(int(binaryNumber, 2) ^ int(weekBinary, 2), len(weekBinary))
        andResult = '{0:0{1}b}'.format(int(xorResult, 2) & int(weekBinary, 2), len(weekBinary))

        for index, bit in enumerate(andResult):
            occupiedSeats[index] += int(bit)

        return andResult.count("1"), occupiedSeats

    def removeFromList(applicantId, listOfApplicants):
        return filter(lambda x: x != applicantId, listOfApplicants)

    def recursion(splaApplicantIds, lhsaApplicantIds, isSpla, lhsaFilledSpaces, splaFilledSpaces, splaMax, lhsaMax, level):
        matchingApplicantsId = list(set(lhsaApplicantIds) & set(splaApplicantIds))

        if isSpla:
            if matchingApplicantsId.__len__() > 0:
                for applicantId in matchingApplicantsId:
                    print 'matching spla'
                    print applicantId
                    count, splaFilledSpaces = calculateDaysForAppliantId(applicantId, splaFilledSpaces, isSpla)
                    print count
                    splaMax, lhsaMax = recursion(removeFromList(applicantId, splaApplicantIds),
                                                 removeFromList(applicantId, lhsaApplicantIds),
                                                 not isSpla, lhsaFilledSpaces, splaFilledSpaces, splaMax + count, lhsaMax, level + 1)

                    print applicantId, splaMax
                    if level == 0:
                        finalSplaMax = splaMax
                        finalId = applicantId
                        splaMax = 0
            else:
                for applicantId in splaApplicantIds:
                    print 'spla'
                    print applicantId
                    count, splaFilledSpaces = calculateDaysForAppliantId(applicantId, splaFilledSpaces, isSpla)
                    print count
                    splaMax, lhsaMax = recursion(removeFromList(applicantId, splaApplicantIds),
                                                 lhsaApplicantIds, not isSpla, lhsaFilledSpaces,
                                                 splaFilledSpaces, splaMax + count, lhsaMax, level + 1)
                    print splaMax, applicantId
                    # if max1 > max:
                    #     max = max1
                    #     finalId = applicantId
        else:
            if matchingApplicantsId.__len__() > 0:
                for applicantId in matchingApplicantsId:
                    print 'lhsa'
                    print applicantId
                    splaMax, lhsaMax = recursion(removeFromList(applicantId, splaApplicantIds),
                                                 removeFromList(applicantId, lhsaApplicantIds),
                                                 not isSpla, lhsaFilledSpaces, splaFilledSpaces, splaMax, lhsaMax, level + 1)

            else:
                for applicantId in lhsaApplicantIds:
                    print 'lhsa'
                    print applicantId
                    splaMax, lhsaMax = recursion(splaApplicantIds, removeFromList(applicantId, lhsaApplicantIds),
                                                 not isSpla, lhsaFilledSpaces, splaFilledSpaces, splaMax, lhsaMax, level + 1)

        return splaMax, lhsaMax

    get_applicant_id_to_week_mapping(data)

    max = 0
    selectedId = None

    # Get already allotted applicants for the next week in binary
    lhsaBinary = binary_number_for_alloted_ids(totalBeds, lhsaFilledSpaces)
    splaBinary = binary_number_for_alloted_ids(totalSpaces, splaFilledSpaces)

    # If all LHSA beds are already full get the best applicant from spla applicants
    if lhsaBinary.count('1') == 7:
        return get_best_applicant_from_list(splaApplicantIds, max, selectedId, splaBinary)

    splaMax, lhsaMax = recursion(splaApplicantIds, lhsaApplicantIds, True, lhsaFilledSpaces, splaFilledSpaces, 0, 0, 0)

    # matchingApplicantsId = list(set(lhsaApplicantIds) & set(splaApplicantIds))
    #     selectedId = get_best_applicant_from_list(matchingApplicantsId, max, selectedId, splaBinary)

    # if selectedId != None:
    #     return selectedId


f = open('output.txt', 'w')
result = calculate_spla_applicant(data)
print result
f.write(result)
f.close()
