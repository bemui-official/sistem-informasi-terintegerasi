from django.shortcuts import render

# Create your views here.
def home (request):
    return render(request, 'home.html')

def team (request):
    return render(request, 'team.html')

def keuangan(request):
    return render(request, 'keuangan.html')

def surat(request):
    return render(request, 'surat.html')

def publikasi(request):
    return render(request, 'publikasi.html')

def survei(request):
    return render(request, 'survei.html')