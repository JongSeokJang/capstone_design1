import re

def preprocess(text):

    target_list = ["\t", "…", "·", "●", "○", "◎", "△", "▲", "◇", "■", "□", ":phone:", "☏", "※", ":arrow_forward:", "▷", "ℓ", "→", "↓", "↑", "┌", "┬", "┐", "├", "┤", "┼", "─", "│", "└", "┴", "┘"]


    for target in target_list:
        text = text.replace(target, " ")    
    regularExpression1 = "\r?\n|\r|\t"
    regularExpression2 = "[a-z0-9_+]+@([a-z0-9-]+\\.)+[a-z0-9]{2,4}|[a-z0-9_+]+@([a-z0-9-]+\\.)+([a-z0-9-]+\\.)+[a-z0-9]{2,4}"
    regularExpression3 = "(file|gopher|news|nntp|telnet|https?|ftps?|sftp):\\/\\/([a-z0-9-]+\\.)+[a-z0-9]{2,4}|(file|gopher|news|nntp|telnet|https?|ftps?|sftp):\\/\\/([a-z0-9-]+\\.)+([a-z0-9-]+\\.)+[a-z0-9]{2,4}"
    #regularExpression4 = "([a-z0-9-]+\\.)+[a-z0-9]{2,4}|([a-z0-9-]+\\.)+([a-z0-9-]+\\.)+[a-z0-9]{2,4}"
    #regularExpression5 = "\\(.*?\\)|\\[.*?\\]|【.*?】|<.*?>"
    #regularExpression6 = "[!@+=%^;:]"
    #regularExpression7 = "[ ]{1,20}"
    regularExpression8 = "[가-힣a-zA-Z][가-힣a-zA-Z][가-힣a-zA-Z] 기자|[가-힣a-zA-Z][가-힣a-zA-Z][가-힣a-zA-Z]기자|[가-힣a-zA-Z][가-힣a-zA-Z] 기자|[가-힣a-zA-Z][가-힣a-zA-Z]기자|[가-힣a-zA-Z][가-힣a-zA-Z][가-힣a-zA-Z][가-힣a-zA-Z] 기자|[가-힣a-zA-Z][가-힣a-zA-Z][가-힣a-zA-Z][가-힣a-zA-Z]기자" 
    
    part1 = re.compile(regularExpression1)
    part2 = re.compile(regularExpression2)
    part3 = re.compile(regularExpression3)
    #part4 = re.compile(regularExpression4)
    #part5 = re.compile(regularExpression5)
    #part6 = re.compile(regularExpression6)
    #part7 = re.compile(regularExpression7)
    part8 = re.compile(regularExpression8)
    text = re.sub(part1, "", text)
    text = re.sub(part2, "", text)
    text = re.sub(part3, "", text)
    #text = re.sub(part4, "", text)
    #text = re.sub(part5, "", text)
    #text = re.sub(part6, " ", text)
    #text = re.sub(part7, " ", text)
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
        textList = textList.replace('.', '. ')
    else:
        textList = ""

    return text
