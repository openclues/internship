from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserAccount(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)



class Coordinator(models.Model):
    user = models.OneToOneField(UserAccount, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(UserAccount, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CareerCenter(models.Model):
    user = models.OneToOneField(UserAccount, primary_key=True, on_delete=models.CASCADE)


class Practise(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    form = models.FileField(upload_to='files', blank=True, null=True)
    due_Time = models.DateTimeField(blank=True, null=True)
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE) #id
    students = models.ManyToManyField(Student, related_name='practises', blank=True)

    def __str__(self):
        return self.title + " " + self.coordinator.user.username


class PractiseSubmission(models.Model):
    UNDER_REVIEW = 0
    APPROVED = 1
    DISPROVE = 2
    STATUS_CHOICES = {
        (APPROVED, "Approved"),
        (DISPROVE, 'Disprove'),
        (UNDER_REVIEW, 'Under Review')
    }

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    uploaded_form = models.FileField(upload_to='submissions', blank=True, null=True)
    note = models.TextField(max_length=500, blank=True, null=True)
