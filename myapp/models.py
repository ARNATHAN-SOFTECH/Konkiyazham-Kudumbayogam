from django.db import models


# ============================================================
# FAMILY MEMBER MODEL
# ============================================================

class FamilyMember(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )

    # Biological / family relationships
    mother = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children_as_mother'
    )

    father = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children_as_father'
    )

    # Legacy parent field.
    # Retained temporarily for compatibility with existing records
    # and code. We can remove it after updating the other files.
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='legacy_children'
    )

    # Family unit connects husband, wife and their children
    family_unit = models.ForeignKey(
        'FamilyUnit',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    note = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default=''
    )

    user = models.OneToOneField(
        'Register',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


# ============================================================
# FAMILY UNIT MODEL
# ============================================================

class FamilyUnit(models.Model):

    husband = models.ForeignKey(
        FamilyMember,
        on_delete=models.CASCADE,
        related_name='husband_units',
        null=True,
        blank=True
    )

    wife = models.ForeignKey(
        FamilyMember,
        on_delete=models.CASCADE,
        related_name='wife_units',
        null=True,
        blank=True
    )

    def __str__(self):

        if self.husband and self.wife:
            return f'{self.husband} & {self.wife}'

        elif self.husband:
            return f'{self.husband} (Single Parent)'

        elif self.wife:
            return f'{self.wife} (Single Parent)'

        return 'Unknown Family'


# ============================================================
# REGISTRATION MODEL
# ============================================================

class Register(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    username = models.CharField(max_length=100)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )

    email = models.EmailField()

    mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    dob = models.DateField()

    country = models.CharField(max_length=100)

    password = models.CharField(max_length=255)

    school = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    qualifications = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    profession = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    # Mother of the registered member
    mother = models.ForeignKey(
        FamilyMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registered_mothers'
    )

    # Father of the registered member
    father = models.ForeignKey(
        FamilyMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registered_fathers'
    )

    relation = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # Spouse name supplied during registration.
    # The actual spouse relationship will be maintained
    # through FamilyUnit.
    spouse = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    married = models.CharField(max_length=200)

    languages = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username


# ============================================================
# ANNOUNCEMENT MODEL
# ============================================================

class Announcement(models.Model):

    title = models.CharField(max_length=200)

    message = models.TextField()

    date = models.DateField()

    issued_by = models.CharField(max_length=100)

    send_notification = models.BooleanField(
        default=False,
        help_text='Tick this box to send announcement email to all members.'
    )

    def __str__(self):
        return self.title
