from django.db import models


class FamilyMember(models.Model):

    name = models.CharField(max_length=100)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 👶 CHILDREN FROM MARRIAGE
    family_unit = models.ForeignKey(
        'FamilyUnit',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children"
    )

    note = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default=""
    )
    
    user = models.OneToOneField(
        'Register',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

# 💍 MARRIAGE MODEL (CORE OF TREE)
class FamilyUnit(models.Model):
    husband = models.ForeignKey(
        FamilyMember,
        on_delete=models.CASCADE,
        related_name="husband_units",
        null=True,
        blank=True
    )

    wife = models.ForeignKey(
        FamilyMember,
        on_delete=models.CASCADE,
        related_name="wife_units",
        null=True,
        blank=True
    )

    def __str__(self):
        if self.husband and self.wife:
            return f"{self.husband} ❤️ {self.wife}"
        elif self.husband:
            return f"{self.husband} (Single Parent)"
        elif self.wife:
            return f"{self.wife} (Single Parent)"
        return "Unknown Family"


class Register(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,
    blank=True,
    null=True
    )
    gender = models.CharField(max_length=10,
    blank=True,
    null=True)
    email = models.EmailField()
    dob = models.DateField()
    country = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    school = models.CharField(max_length=200,
    blank=True,
    null=True)
    qualifications = models.CharField(max_length=100,
    blank=True,
    null=True)
    profession = models.CharField(max_length=200,
    blank=True,
    null=True)

    parent = models.ForeignKey(
        FamilyMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registered_children'
    )

    relation = models.CharField(max_length=100,
    blank=True,
    null=True)
    spouse = models.CharField(
    max_length=100,
    blank=True,
    null=True
    )
    married = models.CharField(max_length=200)
    languages = models.CharField(max_length=200,
    blank=True,
    null=True)
    address = models.TextField(
    blank=True,
    null=True)

    def __str__(self):
        return self.username
    
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateField()
    issued_by = models.CharField(max_length=100)

    def __str__(self):
        return self.title