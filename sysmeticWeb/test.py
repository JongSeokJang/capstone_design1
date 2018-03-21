from cnn_run import predict_unseen_data

content = "아우디 람보르기니 아반떼 스파크 쉐보레"
contents = [content]
print(predict_unseen_data(contents,'trained_model_14'))
