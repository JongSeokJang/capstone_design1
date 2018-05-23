from textblob import TextBlob
from googletrans import Translator
import time
import sys


filename = sys.argv[1]
fp = open(filename, 'r')
content = fp.readlines()
content = ' '.join(content)
fp.close()
translator = Translator()

engString = translator.translate(content,src='ko')
engString = engString.text

analysis = TextBlob(engString)
polarity = analysis.sentiment.polarity
posNeg = ""

if polarity > 0:
    posNeg = "긍정"
elif polarity == 0:
    posNeg = "중립/판별불가"
else:
    posNeg = "부정"

polarity = float(polarity) * 100
print(posNeg)
print("{0:.2f}".format(polarity))
