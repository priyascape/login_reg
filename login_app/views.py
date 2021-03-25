from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt


# -----------------------------------------------------------------------------------------------------------------------
# ROUTE to render home page
# -----------------------------------------------------------------------------------------------------------------------

def index(request):
    return render(request, "index.html")

# ----------------------------------------------------------------------------
# Route to validate, register user and redirect to user page
# ----------------------------------------------------------------------------


def register(request):
    errors = User.objects.basic_validations(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)

        return redirect('/')

    else:
        if request.method == "POST":
            hash1 = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            hash1 = hash1.decode()
            request.session["log_status"] = True
            new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash1)
            request.session['first_name'] = new_user.first_name
            request.session['id'] = new_user.id
            return redirect('/success')

# -----------------------------------------------------------------------------------------------------------------------
# ROUTE to login
# -----------------------------------------------------------------------------------------------------------------------


def login(request):
    errors = User.objects.login_validations(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')

    else:
        user = User.objects.get(email=request.POST['email2'])

        request.session["log_status"] = True
        request.session['id'] = user.id
        request.session['first_name'] = user.first_name

        if bcrypt.checkpw(request.POST['password2'].encode(), user.password.encode()):
            print("password match")

            return redirect('/success')
        else:
            print("failed password")
            return redirect('/')


# -----------------------------------------------------------------------------------------------------------------------
# ROUTE to show user profile
# -----------------------------------------------------------------------------------------------------------------------


def user(request):
    if not request.session["log_status"]:
        messages.warning(request, "Don't Hack Me Please", extra_tags="warning")
        return redirect("/")
    else:

        return render(request, "show.html")


# -----------------------------------------------------------------------------------------------------------------------
# ROUTE to logout of profile
# -----------------------------------------------------------------------------------------------------------------------


def logout(request):
    request.session.clear()
    request.session["log_status"] = False
    return redirect('/')