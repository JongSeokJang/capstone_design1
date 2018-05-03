from cnn_run import predict_unseen_data
import sys

filename = sys.argv[1]
fp = open(filename, 'r')
content = fp.readlines()
content = ' '.join(content)
fp.close()
contentList = [content]
result = predict_unseen_data(contentList, 'trained_model_14')
print(result[0])
