from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Job(models.Model):
    """
    A Job contains all the information associated with an application
    For now most fields are mandatory; this might be revised in future

    Note for future:
    It may be nice to also consider adding entries for Agencies, so
    it would be possible to add agencies, query the job search with the
    agency etc.
    """

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Obsolete', 'Obsolete'),
    )

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    description = models.TextField()
    url = models.CharField(max_length=100)
    job_id = models.CharField(max_length=100)
    agency = models.CharField(max_length=100)
    agency_contact = models.CharField(max_length=100)
    agency_contact_telnum = models.CharField(max_length=100)
    cv = models.FileField()
    cover_letter = models.FileField(blank=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    date_posted = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE) # if User is deleted, delete all jobs

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('jobtracker-home')


class Post(models.Model):
    """
    Each Job can have multiple Posts.
    For now the description field is mandatory

    Note for future:
    Maybe allow description, attachment and URL field; allowing at least one of these, but possibly all
    """
    description = models.TextField()
    attachment = models.FileField(blank=True)  # only allow one attachment per post
    date_posted = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(Job, on_delete=models.CASCADE) # if Post is deleted, delete all posts

    def __str__(self):
        return self.description
