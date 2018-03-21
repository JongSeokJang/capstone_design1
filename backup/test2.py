from textrank import TextRank

fp = open('test2.txt', 'r')
content = fp.readline()
content2 = ""
for c in content:
    content2 = ' '.join(c)
print(content2)
tr = TextRank(window=5, ceof=1.0, content=content)
tr.sentence_rank()

print(tr.sentences(ratio=0.9))
