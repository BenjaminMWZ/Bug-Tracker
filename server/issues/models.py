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


class BugModification(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name='modifications')
    field_modified = models.CharField(max_length=100)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    modified_at = models.DateTimeField()

    def __str__(self):
        return f"Modification for {self.bug.bug_id} on {self.modified_at}"