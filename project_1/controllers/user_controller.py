from django.shortcuts import render
# from project_1.models.home_model import get_message

def index(request):
    return render(request, 'pages/user/index.html')
