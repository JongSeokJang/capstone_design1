from textrank import TextRank
import re
import sys

def preprocess(text):
    target_list = ["\t", "…", "·", "●", "○", "◎", "△", "▲", "◇", "■", "□", ":phone:", "☏", "※", ":arrow_forward:", "▷", "ℓ", "→", "↓", "↑", "┌", "┬", "┐", "├", "┤", "┼", "─", "│", "└", "┴", "┘"]


    for target in target_list:
        text = text.replace(target, " ")    
    regularExpression1 = "\r?\n|\r|\t"
    regularExpression2 = "[a-z0-9_+]+@([a-z0-9-]+\\.)+[a-z0-9]{2,4}|[a-z0-9_+]+@([a-z0-9-]+\\.)+([a-z0-9-]+\\.)+[a-z0-9]{2,4}"
    regularExpression3 = "(file|gopher|news|nntp|telnet|https?|ftps?|sftp):\\/\\/([a-z0-9-]+\\.)+[a-z0-9]{2,4}|(file|gopher|news|nntp|telnet|https?|ftps?|sftp):\\/\\/([a-z0-9-]+\\.)+([a-z0-9-]+\\.)+[a-z0-9]{2,4}"
    regularExpression8 = "[가-힣a-zA-Z][가-힣a-zA-Z][가-힣a-zA-Z] 기자|[가-힣a-zA-Z][가-힣a-zA-Z][가-힣a-zA-Z]기자|[가-힣a-zA-Z][가-힣a-zA-Z] 기자|[가-힣a-zA-Z][가-힣a-zA-Z]기자|[가-힣a-zA-Z][가-힣a-zA-Z][가-힣a-zA-Z][가-힣a-zA-Z] 기자|[가-힣a-zA-Z][가-힣a-zA-Z][가-힣a-zA-Z][가-힣a-zA-Z]기자" 
    
    part1 = re.compile(regularExpression1)
    part2 = re.compile(regularExpression2)
    part3 = re.compile(regularExpression3)
    part8 = re.compile(regularExpression8)
    text = re.sub(part1, "", text)
    text = re.sub(part2, "", text)
    text = re.sub(part3, "", text)
    text = re.sub(part8, "", text)
    

    trimPoint = text.rfind('다.')
    if trimPoint > -1:
        try:
            text = text[0:trimPoint+2]
        except Exception as e:
            print(e)
    if text:
        textList = re.split('\\. |\\.', text)
        textList.pop()
        
        fpStop = open('stopword.txt', 'r')
        stopwords = fpStop.readlines()
        stopwordList = stopwords
        for idx, value in enumerate(stopwordList):
            stopwordList[idx] = stopwordList[idx].replace('\n', '')
        fpStop.close()
        textList = list(map(lambda x: x + '. ', list(filter(lambda x: x in stopwordList, textList))))
            
        textList = (''.join(textList)).strip()
        textList = textList.replace('.', '. ')
    else:
        textList = ""

    return text


content = sys.argv[1]
content = preprocess(content)
tr = TextRank(coef=1.0, window=5, content=content)
tr.sentence_rank()

summarized = ""
for sentence in tr.sentences(ratio=0.3):
    if sentence:
        tmp = sentence[0]
        tmp = tmp.replace('하지만', '')
        tmp = tmp.replace('그러나', '')
        summarized = summarized + tmp + " "


print(summarized)