from django.http import HttpResponse

def check_link(request):
    return HttpResponse('Checking link')

def link(request, pk):
    return HttpResponse('Link')
