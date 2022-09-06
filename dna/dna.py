import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    database = []

    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            database.append(row)

    # TODO: Read DNA sequence file into a variable
    sequence = open(sys.argv[2]).read()

    # TODO: Find longest match of each STR in DNA sequence
    # Prepare the data
    KEYS = []
    for key in database[0].keys():
        KEYS.append(key)

    STR = KEYS
    del STR[0]

    # Find the genome
    genome = []
    for element in range(len(STR)):
        genome.append(str(longest_match(sequence, STR[element])))
    # TODO: Check database for matching profiles
    # Get a dictionary with names as keys and genome as values
    CANDIDATES = {}

    for i in range(len(database)):
        VALUES = []
        for key in KEYS:
            VALUES.append(database[i][key])
            CANDIDATES["{}".format(database[i]["name"])] = VALUES

    # Get a list of names with keys
    NAMES = []
    for key in CANDIDATES.keys():
        NAMES.append(key)

    # loop a list of compare genome with values of candidates and get feedback
    for i in range(len(NAMES)):

        if CANDIDATES[NAMES[i]] == genome:
            print("{}".format(NAMES[i]))
            return 1
    else:
        print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
