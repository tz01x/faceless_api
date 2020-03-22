from django.shortcuts import render

# Create your views here.
def homeview(request):
    template_name='main/index.html'
    return render(request,template_name)
