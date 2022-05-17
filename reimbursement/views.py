import json
from django.shortcuts import render, redirect
from backend.CRUD.crud_kr import kr_create
from backend.misc import firebase_init

fauth = firebase_init.firebaseInit().auth()

def formKr(request):
	try:
		if (request.session['uid']):
			return render(request, 'form_kr.html')
	except:
		return redirect("/user/signin")

def postFormKr(request):
	judul = request.POST.get("judul")
	nama_kegiatan = request.POST.get("nama_kegiatan")
	deskripsi = request.POST.get("deskripsi")
	norek = request.POST.get("norek")
	anrek = request.POST.get("anrek")
	voucher = request.POST.get("link_voucher")
	nominal = request.POST.get("nominal")
	photos = request.POST.get("uploadFiles")
	photos = json.loads(photos)
	print(photos)

	if (photos[0]["successful"] != []):

		photos_meta = []
		for i in photos[0]["successful"]:
			photos_meta.append(i["meta"]["id_firebase"])

		message = kr_create(request, judul, nama_kegiatan, deskripsi, norek, anrek, voucher, nominal, photos_meta)
		if (message == ""):
			return redirect("/")
		else:
			message = "Gagal Upload"
			return redirect(formKr)
	else:
		message = "Gagal Upload"
		return redirect(formKr)