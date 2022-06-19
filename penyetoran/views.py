import json
from django.shortcuts import render, redirect
from backend.CRUD.crud_ks import ks_create
from backend.misc import firebase_init

fauth = firebase_init.firebaseInit().auth()

def formKs(request):
	try:
		if (request.session['uid']):
			if (fauth.get_account_info(request.session['uid'])):
				return render(request, 'form_ks.html')
			else:
				return redirect("/user/logout")
	except:
		return redirect("/user/signin")

def postFormKs(request):
	judul = request.POST.get("judul")
	nama_proker = request.POST.get("nama_proker")
	nama_kegiatan = request.POST.get("nama_kegiatan")
	deskripsi = request.POST.get("deskripsi")
	voucher = request.POST.get("link_voucher")
	nominal_setor = request.POST.get("nominal_setor")
	nominal_diterima = request.POST.get("nominal_diterima")
	photos = request.POST.get("uploadFiles")
	photos = json.loads(photos)
	print(photos)

	if (photos[0]["successful"] != []):

		photos_meta = []
		for i in photos[0]["successful"]:
			photos_meta.append(i["meta"]["id_firebase"])

		message = ks_create(request, judul, nama_proker, nama_kegiatan, deskripsi, voucher, nominal_setor, nominal_diterima, photos_meta)
		if (message == ""):
			return redirect("/")
		else:
			message = "Gagal Upload"
			return redirect(formKs)
	else:
		message = "Gagal Upload"
		return redirect(formKs)