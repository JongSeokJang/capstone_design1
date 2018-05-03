from textblob import TextBlob
import sys

filename = sys.argv[1]
fp = open(filename, 'r')
content = fp.readlines()
content = ' '.join(content)
fp.close()

analysis = TextBlob(content)
polarity = analysis.sentiment.polarity
polarity = float(polarity) * 100
posNeg = ""
if polarity >= 0:
    posNeg = "POSITIVE"
else:
    posNeg = "NEGATIVE"
print(posNeg)
print("{0:.2f}".format(polarity))