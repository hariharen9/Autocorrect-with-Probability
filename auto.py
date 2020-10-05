import pandas as pd
import numpy as np
import textdistance
import re
from collections import Counter
words = []  # please use utf8 format
with open('words.txt', 'r', encoding="utf8") as f:
    file_name_data = f.read()
    file_name_data = file_name_data.lower()
    words = re.findall('\w+', file_name_data)
# This is our vocabulary
V = set(words)
print("Do you want to see all the words in the dictionary? Y/N")
ans = input()
ans = str(ans).lower()
if ans == "y":
    print(f"The first ten words in the text are: \n{words[0:]}\n")
else:
    print(f"There are {len(V)} unique words in the vocabulary.\n")

word_freq_dict = {}
word_freq_dict = Counter(words)

print("-------Some common words in the given file and their number of occurances are -------\n")
print(word_freq_dict.most_common()[0:15])

probs = {}
Total = sum(word_freq_dict.values())
for k in word_freq_dict.keys():
    probs[k] = word_freq_dict[k]/Total


def my_autocorrect(input_word):
    input_word = input_word.lower()

    if input_word in V:
        return('Your word seems to be correct')
    else:
        similarities = [1-(textdistance.Jaccard(qval=2).distance(v, input_word))
                        for v in word_freq_dict.keys()]
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df = df.rename(columns={'index': 'Word', 0: 'Probability'})
        df['Similarity'] = similarities
        output = df.sort_values(
            ['Similarity', 'Probability'], ascending=False).head()
        return(output)


word = input("\nEnter the Word: \n")
result = my_autocorrect(word)
print(result)
