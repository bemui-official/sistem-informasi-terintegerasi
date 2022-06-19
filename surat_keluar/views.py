from django.shortcuts import render, redirect
from backend.CRUD.crud_sk import sk_create
from backend.misc import firebase_init

fauth = firebase_init.firebaseInit().auth()

def formSk(request):
	try:
		if (request.session['uid']):
			if (fauth.get_account_info(request.session['uid'])):
				return render(request, 'form_sk.html')
			else:
				return redirect("/user/logout")
	except:
		return redirect("/user/signin")

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

