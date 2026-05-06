from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

           
            admin_message = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Message: {message}
"""

            send_mail(
                subject='New Contact Form Submission',
                message=admin_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['arnathansoftech7@gmail.com'],
                fail_silently=False,
            )

           
            user_message = f"""
Hi {name},

Thank you for contacting us. We have received your message and will get back to you soon.


Regards,
Team Konkiyazhikam Kudumbayogam
"""

            send_mail(
                subject='Thank You for Contacting Us',
                message=user_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email], 
                fail_silently=False,
            )

            return redirect('success')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})






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
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)

            if 'hobbies' in form.cleaned_data:
                user.hobbies = ",".join(form.cleaned_data['hobbies'])

            user.save()

           
            first_name = user.first_name
            last_name = user.last_name
            email = user.email
            country = user.country
            profession = user.profession

            
            user_subject = "Registration Successful"
            user_message = f"""
Dear {first_name},

Thank you for registering with Konkiyazhikam Kudumbayogam.

We have successfully received your registration.

Regards,
Konkiyazhikam Kudumbayogam
"""

            
            admin_subject = "New User Registration"
            admin_message = f"""
New user registered:

Name: {first_name} {last_name}
Email: {email}
Country: {country}
Profession: {profession}
"""

            try:
                
                send_mail(
                    user_subject,
                    user_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                # Send email to ADMIN
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['arnathansoftech7@gmail.com'],  
                    fail_silently=False,
                )

                return redirect('register_success')

            except Exception as e:
                print("EMAIL ERROR:", e)
                messages.warning(
                    request,
                    "Registered successfully, but email sending failed."
                )
                return redirect('register_success')

    else:
        form = RegisterForm()

    return render(request, "register.html", {'form': form})

def register_success(request):
    return render(request, 'register_success.html')