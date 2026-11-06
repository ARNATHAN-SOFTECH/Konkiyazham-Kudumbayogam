
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from meta.views import Meta

from .forms import ContactForm, RegisterForm
from .models import FamilyMember, Register, FamilyUnit, Announcement


# ============================================================
# CONTACT
# ============================================================

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


# ============================================================
# GENERAL PAGES
# ============================================================

def gallery(request):
    return render(request, "gallery.html")


def about(request):
    return render(request, "about.html")


def community_updates(request):
    return render(request, "community-updates.html")


def home(request):

    today = timezone.localdate()

    birthdays_today = Register.objects.filter(
        dob__month=today.month,
        dob__day=today.day
    )

    meta = Meta(
        title='Konkiyazham Kudumbasangam',
        description='Official website of Konkiyazham Kudumbasangam with family tree, registrations, events and updates.',
        keywords=['Kudumbasangam', 'Kerala family', 'family tree'],
    )

    return render(
        request,
        'home.html',
        {
            'meta': meta,
            'birthdays_today': birthdays_today
        }
    )


def donations(request):
    return render(request, "donations.html")


def login(request):
    return render(request, "login.html")


def starter_page(request):
    return render(request, "starter-page.html")


def vision(request):
    return render(request, "vision.html")


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


# ============================================================
# ANNOUNCEMENTS
# ============================================================

def announcement_view(request):

    announcements = Announcement.objects.all().order_by('-date')

    return render(
        request,
        'announcement.html',
        {'announcements': announcements}
    )


# ============================================================
# FAMILY TREE
# ============================================================


def familytree(request):

    # Root couples: both have no recorded parents,
    # and the family unit has at least one child.
    roots = FamilyUnit.objects.filter(
        husband__isnull=False,
        wife__isnull=False,
        husband__mother__isnull=True,
        husband__father__isnull=True,
        wife__mother__isnull=True,
        wife__father__isnull=True,
        children__isnull=False
    ).distinct()

    # Root individuals: no parents and no spouse,
    # but connected to children through a single-parent unit.
    root_members = FamilyMember.objects.filter(
        mother__isnull=True,
        father__isnull=True
    ).filter(
        Q(
            husband_units__wife__isnull=True,
            husband_units__children__isnull=False
        ) |
        Q(
            wife_units__husband__isnull=True,
            wife_units__children__isnull=False
        )
    ).distinct().order_by('name')

    return render(
        request,
        "familytree.html",
        {
            "roots": roots,
            "root_members": root_members
        }
    )


# ============================================================
# REGISTRATION
# ============================================================

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            try:

                with transaction.atomic():

                    cleaned_data = form.cleaned_data

                    # ========================================
                    # 1. GET EXISTING PARENTS
                    # ========================================

                    mother_member = cleaned_data.get('mother')
                    father_member = cleaned_data.get('father')

                    # ========================================
                    # 2. CREATE NEW MOTHER IF SELECTED
                    # ========================================

                    if cleaned_data.get('mother_is_new'):

                        mother_name = cleaned_data.get(
                            'mother_new_name'
                        ).strip()

                        mother_member = FamilyMember.objects.create(
                            name=mother_name,
                            gender='Female',
                            note='Added during registration'
                        )

                    # ========================================
                    # 3. CREATE NEW FATHER IF SELECTED
                    # ========================================

                    if cleaned_data.get('father_is_new'):

                        father_name = cleaned_data.get(
                            'father_new_name'
                        ).strip()

                        father_member = FamilyMember.objects.create(
                            name=father_name,
                            gender='Male',
                            note='Added during registration'
                        )

                    # ========================================
                    # 4. SAVE REGISTRATION
                    # ========================================

                    user = form.save(commit=False)

                    user.mother = mother_member
                    user.father = father_member

                    user.save()

                    # ========================================
                    # 5. CREATE / UPDATE FAMILY MEMBER
                    # ========================================

                    full_name = (
                        f"{user.first_name} {user.last_name or ''}"
                    ).strip()

                    member, created = FamilyMember.objects.get_or_create(
                        user=user,
                        defaults={
                            'name': full_name,
                            'gender': user.gender,
                            'note': user.profession or ''
                        }
                    )

                    if not created:

                        member.name = full_name
                        member.gender = user.gender
                        member.note = user.profession or ''

                    # Connect parents.
                    member.mother = mother_member
                    member.father = father_member

                    # Keep legacy parent field for compatibility.
                    member.parent = father_member or mother_member

                    member.save()

                    # ========================================
                    # 6. CREATE PARENTS' FAMILY UNIT
                    # ========================================

                    parent_unit = None

                    if mother_member or father_member:

                        parent_unit, _ = FamilyUnit.objects.get_or_create(
                            husband=father_member,
                            wife=mother_member
                        )

                    # Connect the registered member to parents' unit.
                    member.family_unit = parent_unit

                    member.save(update_fields=['family_unit'])

                    # ========================================
                    # 7. CREATE / CONNECT SPOUSE
                    # ========================================

                    if user.spouse and user.gender in ['Male', 'Female']:

                        spouse_name = user.spouse.strip()

                        if spouse_name:

                            spouse_gender = (
                                'Female'
                                if user.gender == 'Male'
                                else 'Male'
                            )

                            spouse_member, _ = (
                                FamilyMember.objects.get_or_create(
                                    name__iexact=spouse_name,
                                    gender=spouse_gender,
                                    defaults={
                                        'name': spouse_name,
                                        'note': 'Spouse'
                                    }
                                )
                            )

                            if user.gender == 'Male':

                                FamilyUnit.objects.get_or_create(
                                    husband=member,
                                    wife=spouse_member
                                )

                            else:

                                FamilyUnit.objects.get_or_create(
                                    husband=spouse_member,
                                    wife=member
                                )

                    # ========================================
                    # 8. EMAIL DETAILS
                    # ========================================

                    first_name = user.first_name
                    last_name = user.last_name or ''
                    email = user.email
                    country = user.country
                    profession = user.profession or ''

                    user_subject = "Registration Completed"

                    user_message = f"""
Dear {first_name},

Thank you for registering with Konkiyazhikam Kudumbayogam.

Your registration has been completed successfully.

Your family relationships:

Mother: {mother_member.name if mother_member else "Not Selected"}
Father: {father_member.name if father_member else "Not Selected"}

Your profile has been connected to the family tree.

Regards,
Konkiyazhikam Kudumbayogam
"""

                    admin_subject = "New User Registration"

                    admin_message = f"""
New user registered:

Name: {first_name} {last_name}
Gender: {user.gender or "Not Provided"}
Email: {email}
Mobile: {user.mobile or "Not Provided"}
Country: {country}
Profession: {profession}

Mother: {mother_member.name if mother_member else "Not Selected"}
Father: {father_member.name if father_member else "Not Selected"}
Spouse: {user.spouse or "Not Provided"}
"""

                # ============================================
                # 9. SEND EMAILS AFTER DATABASE SAVE
                # ============================================

                try:

                    send_mail(
                        subject=user_subject,
                        message=user_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )

                    send_mail(
                        subject=admin_subject,
                        message=admin_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[
                            "arnathansoftech7@gmail.com"
                        ],
                        fail_silently=False,
                    )

                except Exception as email_error:

                    print("EMAIL ERROR:", email_error)

                return redirect("register_success")

            except Exception as e:

                print("REGISTRATION ERROR:", e)

                form.add_error(
                    None,
                    "Registration could not be completed. Please try again or contact the administrator."
                )

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )

# ============================================================
# REGISTRATION SUCCESS
# ============================================================

def register_success(request):

    return render(request, 'register_success.html')


# ============================================================
# ROBOTS.TXT
# ============================================================

def robots_txt(request):

    lines = [
        "User-Agent: *",
        "Allow: /",
        "Sitemap: https://www.konkiyazhikamkudumbayogam.com/sitemap.xml"
    ]

    return HttpResponse(
        "\n".join(lines),
        content_type="text/plain"
    )


# ============================================================
# DAILY BIRTHDAY WISHES
# ============================================================

def send_birthday_wishes(request=None):

    today = timezone.localdate()

    members = Register.objects.filter(
        dob__month=today.month,
        dob__day=today.day
    )

    print("Birthdays found:", members.count())

    sent_count = 0

    for member in members:

        print("Processing:", member.first_name)
        print("Email:", member.email)

        if member.email:

            try:

                send_mail(
                    subject="🎂 Happy Birthday from Konkiyazhikam Kudumbayogam",

                    message=(
                        f"Dear {member.first_name},\n\n"
                        "Wishing you a very Happy Birthday 🎂🎉\n"
                        "May your day be filled with joy and blessings.\n\n"
                        "- Konkiyazhikam Kudumbayogam Team\n\n"
                        "🎁 View today's birthday celebrations:\n"
                        "https://www.konkiyazhikamkudumbayogam.com/birthday-wish/\n"
                    ),

                    from_email=getattr(
                        settings,
                        "EMAIL_HOST_USER",
                        "noreply@example.com"
                    ),

                    recipient_list=[member.email],
                    fail_silently=False,
                )

                print(f"[EMAIL SENT] {member.email}")

                sent_count += 1

            except Exception as e:

                print(f"[EMAIL FAILED] {member.email}")
                print(e)

    return JsonResponse({
        "status": "success",
        "sent": sent_count
    })


# ============================================================
# SMS FUNCTION
# ============================================================

def send_birthday_sms(phone, name):

    message = (
        f"Happy Birthday {name}, "
        "Here's to another trip around the sun!\n\n"
        "– Konkiyazhikam Kudumbayogam Team"
    )

    print(f"[SMS SENT] {phone} -> {message}")


# ============================================================
# BIRTHDAY WISH PAGE
# ============================================================

def birthday_wish(request):

    today = timezone.localdate()

    birthdays_today = Register.objects.filter(
        dob__month=today.month,
        dob__day=today.day
    )

    context = {
        "birthdays_today": birthdays_today,
        "today": today
    }

    return render(request, 'birthday_wish.html', context)
