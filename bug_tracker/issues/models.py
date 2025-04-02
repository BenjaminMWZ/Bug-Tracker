from django.db import models

# This file defines the models for the bug tracking system.
# The main model is Bug, which represents a bug report.
# Each bug has a unique ID, subject, description, status, priority, and timestamps for creation and updates.
# The status and priority fields are defined with choices to limit the values that can be assigned.
# The Bug model also includes a modified_count field to track the number of times the bug has been modified.
# The __str__ method is overridden to provide a readable string representation of the Bug instance.
class Bug(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    bug_id = models.CharField(max_length=50, unique=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    modified_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.bug_id}: {self.subject}"