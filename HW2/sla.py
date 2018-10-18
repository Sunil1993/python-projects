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
    binaryString = ''
    for x in binaryArray:
        if x >= total:
            binaryString += '1'
        else:
            binaryString += '0'
    return binaryString


# Calculate the first applicant from set of applicants
def calculate_spla_applicant(data):
    idToWeekMap = {}
    lhsaApplicantIds = []
    splaApplicantIds = []

    # array binary which represents next 7 days allotment
    lhsaBinaryArray = [0] * 7
    splaBinaryArray = [0] * 7

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

    # Applicants matching both LHSA and SPLA
    matchingApplicants = []

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
                    lhsaBinaryArray[index] += int(item)
                continue

            if (selectedSPLAIds.__contains__(id)):
                for index, item in enumerate(week):
                    splaBinaryArray[index] += int(item)
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

    get_applicant_id_to_week_mapping(data)

    max = 0
    selectedId = None

    # Get already allotted applicants for the next week in binary
    lhsaBinary = binary_number_for_alloted_ids(totalBeds, lhsaBinaryArray)
    splaBinary = binary_number_for_alloted_ids(totalSpaces, splaBinaryArray)

    # If all LHSA beds are already full do not check for intersection
    if lhsaBinary.count('1') != 7:
        matchingApplicantsId = list(set(lhsaApplicantIds) & set(splaApplicantIds))
        selectedId = get_best_applicant_from_list(matchingApplicantsId, max, selectedId, splaBinary)

    if selectedId != None:
        return selectedId

    return get_best_applicant_from_list(splaApplicantIds, max, selectedId, splaBinary)


f = open('output.txt', 'w')
result = calculate_spla_applicant(data)
print result
f.write(result)
f.close()
