from django.shortcuts import redirect, render
from backend.CRUD.crud_publikasi import publikasi_read

from home.forms import SearchPublicationRequest

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
    form = SearchPublicationRequest()
    if(request.method != "POST"):
        return render(request, 'publikasi.html', {'form' : form})
    else:
        id_pub_request = request.POST.get("id_pub_request")
        data = publikasi_read(id_pub_request)
        if(not data): 
            error_msg = f"Maaf, publikasi dengan identifikasi ({id_pub_request}) tidak ada. \nMohon dicoba kembali dengan identifikasi yang benar."
            return render(request, 'publikasi.html', {'form' : form, 'error_msg': error_msg})
        else:
            return redirect(f"../publikasi/detail/{id_pub_request}")
def survei(request):
    return render(request, 'survei.html')