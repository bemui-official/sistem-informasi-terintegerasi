from django.shortcuts import render, get_object_or_404, redirect, reverse
from backend.crud_user import user_create, user_read, user_delete
from django.contrib import auth
from backend import firebase_init

fauth = firebase_init.firebaseInit().auth()

def signUp(request):
	return render(request, 'signUp.html')

def postSignUp(request):
	idBirdep = request.POST.get("username")
	email = request.POST.get("email")
	password = request.POST.get("password1")
	password2 = request.POST.get("password2")
	asal = request.POST.get("asal")
	nama = request.POST.get("nama")
	panggilan = request.POST.get("panggilan")
	permintaan = []
	if (password == password2):
		message = user_create(idBirdep, email, password, asal, nama, 0, panggilan, permintaan)
	if message == "":
		return redirect(signIn)
	else:
		return redirect(signUp)

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
	return redirect('/')

def logout(request):
	auth.logout(request)
	return redirect(signIn)

