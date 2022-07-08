from django.shortcuts import render, redirect
from backend.CRUD.crud_user import user_create, user_read
from backend.CRUD.crud_dashboard import read_requests
from django.contrib import auth
from backend.misc import firebase_init
from backend.constants.birdeptim import pi, birdeptim, kode_fungsionaris

fauth = firebase_init


# ---------------------
# Authentication
# --------------------
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
	print(user)
	session_id = user['idToken']
	request.session['uid'] = str(session_id)
	request.session['dashboard'] = "https://www.google.com"
	print(request.session['uid'])
	return redirect('/')

def logout(request):
	auth.logout(request)
	return redirect("user:signin")


# ---------------------
# Dashboard
# --------------------
def dashboard(request):
	if (request.session['uid']):
		user_session = fauth.get_account_info(request.session['uid'])
		if (user_session):
			user = user_read(user_session['users'][0]['localId'])
			print(user['id'])
			data = read_requests(user['id'])
			return render(request, 'dashboard.html', {
				'data': data,
			})
		else:
			return redirect("/user/logout")
	# except:
	#     return redirect("/user/signin")
