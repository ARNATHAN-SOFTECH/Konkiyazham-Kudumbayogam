from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

from django.urls import path
from . import views
from .forms import RegisterForm
from .models import FamilyMember, FamilyUnit, Announcement
from django.contrib import messages

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




def gallery(request): return render(request, "gallery.html")

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

def calendar(request):
    return render(request, 'calendar.html')

def announcement_view(request):
    announcement_view = Announcement.objects.all().order_by('-date')

    return render(request, 'announcement.html', {
        'announcements': announcement_view
    })

def familytree(request):
    roots = FamilyMember.objects.filter(parent__isnull=True,     wife_units__isnull=True,
).exclude(note="Spouse")

    return render(request, "familytree.html", {
        "roots": roots
    })






def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.save()

            # =========================
            # AUTO ADD TO FAMILY TREE
            # =========================

            parent_member = user.parent

            if parent_member:

                full_name = f"{user.first_name} {user.last_name or ''}".strip()

                # MAIN MEMBER
                member = FamilyMember.objects.create(
                    name=full_name,
                    parent=parent_member,
                    note=user.profession or "",
                    user=user
                )

                # =========================
                # CREATE SPOUSE
                # =========================

                if user.spouse:

                    spouse_member = FamilyMember.objects.create(
                        name=user.spouse,
                        note="Spouse"
                    )

                    # =========================
                    # CREATE FAMILY UNIT
                    # =========================

                    if user.gender == "Male":

                        FamilyUnit.objects.create(
                            husband=member,
                            wife=spouse_member
                        )

                    else:

                        FamilyUnit.objects.create(
                            husband=spouse_member,
                            wife=member
                        )

            # =========================
            # EMAIL SECTION
            # =========================

            first_name = user.first_name
            last_name = user.last_name
            email = user.email
            country = user.country
            profession = user.profession

            if parent_member:

                user_subject = "Successfully Added to Family Tree"

                user_message = f"""
            Dear {first_name},

            Thank you for registering with Konkiyazhikam Kudumbayogam.

            Your registration has been successfully completed and your profile has been connected to the Family Tree.

            We are happy to welcome you to our family community.

            Regards,
            Konkiyazhikam Kudumbayogam
            """

            else:

                user_subject = "Registration Completed"

                user_message = f"""
            Dear {first_name},

            Thank you for registering with Konkiyazhikam Kudumbayogam.

            Your registration has been received successfully.

            However, your profile has not yet been connected to the Family Tree because a parent/member connection was not selected during registration.

            You may register again later with proper family connection details, or contact the admin for assistance in connecting your family branch.

            Regards,
            Konkiyazhikam Kudumbayogam
            """

            admin_subject = "New User Registration"

            admin_message = f"""
New user registered:

Name: {first_name} {last_name or ""}
Email: {email}
Country: {country}
Profession: {profession}
Parent Name: {parent_member.name if parent_member else "Not Selected"}
"""

            try:

                send_mail(
                    user_subject,
                    user_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['arnathansoftech7@gmail.com'],
                    fail_silently=False,
                )

            except Exception as e:
                print("EMAIL ERROR:", e)

            return redirect('register_success')

    else:

        form = RegisterForm()

    return render(request, "register.html", {'form': form})

def register_success(request):
    return render(request, 'register_success.html')