from django.shortcuts import render, redirect
from backend.CRUD.crud_user import user_create
from django.contrib import auth
from backend.misc import firebase_init
from backend.constants.birdeptim import pi, birdeptim, kode_fungsionaris

fauth = firebase_init.firebaseInit().auth()

def signUp(request):
	return render(request, 'signUp.html', {
		"pi": pi,
		"birdeptim": birdeptim,
		"kode_fungsionaris": kode_fungsionaris
	})

def postSignUp(request):
	idBirdep = request.POST.get("username")
	email = request.POST.get("email")
	password = request.POST.get("password1")
	password2 = request.POST.get("password2")
	asal = request.POST.get("asal")
	nama = request.POST.get("nama")
	panggilan = request.POST.get("panggilan")
	birdeptim = request.POST.get("birdeptim")
	permintaan = []
	if (password == password2):
		message = user_create(idBirdep, email, password, asal, nama, 0, panggilan, permintaan, birdeptim)
	if message == "":
		return redirect("user:signin")
	else:
		return redirect("user:signup")

def signIn(request):
	return render(request, 'signIn.html')

def postSignIn(request):
	email = request.POST.get("email")
	password = request.POST.get("password")
	try:
		user = fauth.sign_in_with_email_and_password(email, password)
	except:
		return redirect(signIn)
	print(fauth.current_user)
	session_id = user['idToken']
	request.session['uid'] = str(session_id)
	request.dashboard = "https://www.google.com"
	return redirect('/')

def logout(request):
	auth.logout(request)
	return redirect("user:signin")

