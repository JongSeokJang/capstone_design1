from gensim.models import word2vec
import sys
import json
model = word2vec.Word2Vec.load("./model/digitaltimes.model")

word = sys.argv[1]
result = model.wv.most_similar(positive=[word])
result = json.dumps(result, ensure_ascii=False)
print(result)
