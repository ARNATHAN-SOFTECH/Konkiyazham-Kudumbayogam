
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.urls import path
from . import views

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            full_message = f"""
            Name: {name}
            Email: {email}
            Message: {message}
            """

            send_mail(
                subject='New Contact Form Submission',
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['your_email@gmail.com'],  
            )

            return redirect('success') 

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})






def successview(request):
    return render(request, "success.html")

def finance(request):
    return render(request,"finance.html")

def community_updates(request):
    return render(request,"community-updates.html")

def home(request):
    return render(request,"home.html")

def donations(request):
    return render(request,"donations.html")

def login(request):
    return render(request,"login.html")

def starter_page(request):
    return render(request,"starter-page.html")

def vision(request):
    return render(request,"vision.html")

def chathanoor(request):
    return render(request, 'chathanoor.html')

def kollam(request):
    return render(request, 'kollam.html')

def kottiyam(request):
    return render(request, 'kottiyam.html')

def veliyam(request):
    return render(request, 'veliyam.html')

def attingal(request):
    return render(request, 'attingal.html')

def trivandrum(request):
    return render(request, 'trivandrum.html')

def bangalore(request):
    return render(request, 'bangalore.html')

def success(request):
    return render(request, "success.html")

def familytree(request):
    return render(request, "familytree.html")





from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)

            # Optional: handle hobbies if multiple
            if 'hobbies' in form.cleaned_data:
                user.hobbies = ",".join(form.cleaned_data['hobbies'])

            user.save()

            first_name = user.first_name
            last_name = user.last_name
            email = user.email
            country = user.country

            subject = "Registration Successful"
            message = f"""
Dear {first_name},

Thank you for registering with Konkiyazhikam Kudumbayogam.

Registration Details:
Name: {first_name} {last_name}
Email: {email}
Country: {country}

We are happy to welcome you to our community.

Regards,
Konkiyazhikam Kudumbayogam
"""

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return redirect('register_success')

    else:
        form = RegisterForm()

    return render(request, "register.html", {'form': form})


def register_success(request):
    return render(request, 'register_success.html')





















