from django.db import models

class Bug(models.Model):
    bug_id = models.CharField(max_length=50, unique=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    modified_count = models.IntegerField()

    def __str__(self):
        return self.bug_id
