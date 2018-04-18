from textrank import TextRank
import json
import sys

filename = sys.argv[1]
fp = open(filename, 'r')
content = fp.readlines()
content = ' '.join(content)
fp.close()
tr = TextRank(ceof=1.0, window=5, content=content)
tr.keyword_rank()
result = tr.keywords(num=5)
result = json.dumps(result, ensure_ascii=False)
print(result)
