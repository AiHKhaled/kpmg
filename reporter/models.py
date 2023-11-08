from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    CHOICES = [
        ('Active', 'Active'),
        ('Draft', 'Draft'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=10, choices=CHOICES, default='Draft')
    cost = models.IntegerField(null=True)
    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    TASKS = [
        ("To Do", "To Do"),
        ("In Progress", "In Progress"),
        ("Done", "Done"),
        ("Cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=15, choices=TASKS, default="To Do")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name