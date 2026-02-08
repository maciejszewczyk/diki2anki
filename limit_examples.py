import csv
from collections import defaultdict

INPUT_FILE = "sentences.csv"
OUTPUT_FILE = "sentences_3examples.csv"
MAX_EXAMPLES_PER_WORD = 3


def limit_examples_per_word():
    counts = defaultdict(int)

    with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as infile, \
         open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as outfile:

        reader = csv.reader(infile, delimiter=";")
        writer = csv.writer(outfile, delimiter=";")

        for row in reader:
            if len(row) != 3:
                # skip malformed rows silently
                continue

            word, tr, en = row

            if counts[word] < MAX_EXAMPLES_PER_WORD:
                writer.writerow([word, tr, en])
                counts[word] += 1


if __name__ == "__main__":
    limit_examples_per_word()
