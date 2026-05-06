from django.db import models

class Register(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    dob = models.DateField()
    country = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    school = models.CharField(max_length=200)
    qualifications = models.CharField(max_length=100)
    profession = models.CharField(max_length=200)
    parents = models.CharField(max_length=200)
    relation = models.CharField(max_length=100)
    spouse = models.CharField(max_length=100)
    married = models.CharField(max_length=200)
    languages = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return self.username
    
    


     

