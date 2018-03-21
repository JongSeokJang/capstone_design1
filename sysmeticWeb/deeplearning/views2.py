from django.shortcuts import render
from cnn_run import predict_unseen_data
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def deep(request):
    return render(request, 'deeplearning/index.html', {})

def result(request):
    if request.method=="POST":
        content = request.POST['content']
        contentList = [content]
        result = predict_unseen_data(contentList, 'trained_model_14')
        result = result[0]
        mystring = "입력한 뉴스 원문입니다."
        return render(request, 'deeplearning/index.html', {'result': result, 'content': content, 'mystring': mystring})
