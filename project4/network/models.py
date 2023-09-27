from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


# Bug Model
class Bug(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('fixed', 'Fixed'),
        ('under_review', 'Under Review'),
    )
    SEVERITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='low')
    screenshot = models.ImageField(upload_to='network/static/bug_images/', null=True, blank=True)
    steps_to_reproduce = models.TextField()
    comments = models.ManyToManyField('BugComment', related_name='bug_comments', blank=True)

    # You can associate the bug with a reporter (user who reported the bug)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.id}: {self.title}/n  {self.description}/n {self.status} /n {self.severity}/n {self.screenshot} /n {self.steps_to_reproduce} /n {self.comments} /n {self.reporter}"

# Bug Comment Model
class BugComment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.commenter} on {self.comment_time}'

# Developer Model
class Developer(models.Model):
    email = models.EmailField(unique=True)  # Make sure null=True is not set
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} /n {self.email}'

# Assigned Developer Model
class AssignedDeveloper(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    date_assigned = models.DateField(default=timezone.now)

    def __str__(self):
        return f'Developer: {self.developer}, Bug: {self.bug}, Assigned On: {self.date_assigned}'

# Change Status Model
class ChangeStatus(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Bug.STATUS_CHOICES)
    comment = models.TextField()
    change_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Change Status of Bug: {self.bug} to {self.status} on {self.change_time}'