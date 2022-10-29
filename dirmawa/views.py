import json
from django.shortcuts import render, redirect
from backend.CRUD.crud_sd import sd_create
from backend.misc import firebase_init

fauth = firebase_init.firebaseInit().auth()

def formSd(request):
	try:
		if (request.session['uid']):
			if (fauth.get_account_info(request.session['uid'])):
				return render(request, 'form_sd.html')
			else:
				return redirect("/user/logout")
	except:
		return redirect("/user/signin")

def postFormSd(request):
	judul = request.POST.get("judul")
	nama_proker = request.POST.get("nama_proker")
	nama_kegiatan = request.POST.get("nama_kegiatan")
	deskripsi = request.POST.get("deskripsi")
	jenis = request.POST.get("jenis")
	file = request.POST.get("uploadFiles")
	file = json.loads(file)
	print(file)

	if (file[0]["successful"] != []):

		file_meta = []
		for i in file[0]["successful"]:
			file_meta.append(i["meta"]["id_firebase"])

		message = sd_create(request, judul, nama_proker, nama_kegiatan, deskripsi, jenis, file_meta)
		if (message == ""):
			return redirect("/")
		else:
			message = "Gagal Upload"
			return redirect(formSd)
	else:
		message = "Gagal Upload"
		return redirect(formSd)