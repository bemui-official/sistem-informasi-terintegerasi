from django.shortcuts import render, get_object_or_404, redirect, reverse
from backend.crud_sk import sk_create
from django.contrib import auth
from backend import firebase_init


fauth = firebase_init.firebaseInit().auth()

def formSk(request):
	return render(request, 'form_sk.html')

def postFormSk(request):
	judul = request.POST.get("judul")
	nama_kegiatan = request.POST.get("nama_kegiatan")
	deskripsi = request.POST.get("deskripsi")
	jenis_surat = request.POST.get("jenis")
	link = request.POST.get("linkdocs")

	message = sk_create(request, judul, nama_kegiatan, deskripsi, jenis_surat, link)
	print(message)
	if message == "":
		return redirect("/")
	else:
		return redirect(formSk)

