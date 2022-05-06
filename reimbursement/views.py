from django.shortcuts import render, get_object_or_404, redirect, reverse
from backend.crud_kr import kr_create
from django.contrib import auth
from backend import firebase_init


fauth = firebase_init.firebaseInit().auth()

def formKr(request):
	return render(request, 'form_kr.html')

def postFormKr(request):
	judul = request.POST.get("judul")
	nama_kegiatan = request.POST.get("nama_kegiatan")
	deskripsi = request.POST.get("deskripsi")
	norek = request.POST.get("norek")
	anrek = request.POST.get("anrek")
	voucher = request.POST.get("link_voucher")
	nominal = request.POST.get("nominal")
	photos = request.POST.get("uploadFiles")
	print(photos)
	print(judul)


	# message = kr_create(request, judul, nama_kegiatan, deskripsi, norek, anrek, voucher, nominal)
	# print(message)
	# if message == "":
	# 	return redirect("/")
	# else:
	# 	return redirect(formKr)

