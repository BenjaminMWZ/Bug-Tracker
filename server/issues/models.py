from django.db import models

class Bug(models.Model):
    """
    Model representing a bug report in the system.
    
    This class stores information about bugs including their unique ID,
    description, status, priority, and modification history. It serves as
    the core data structure for the bug tracking functionality.
    
    Bugs can be created manually through the API or automatically via
    email processing. They go through different status stages during their
    lifecycle from open to closed.
    """
    
    # Available status options for bugs in the system
    STATUS_CHOICES = [
        ('open', 'Open'),  # Bug is newly reported and not yet addressed
        ('in_progress', 'In Progress'),  # Bug is currently being worked on
        ('resolved', 'Resolved'),  # Bug has been fixed but not verified
        ('closed', 'Closed'),  # Bug is completely addressed and verified
    ]
    
    # Available priority levels for bugs
    PRIORITY_CHOICES = [
        ('low', 'Low'),  # Minor issues, can be addressed when convenient
        ('medium', 'Medium'),  # Important issues that should be fixed in due course
        ('high', 'High'),  # Critical issues requiring immediate attention
    ]
    
    # Unique identifier for the bug, often follows a pattern like BUG-1234
    bug_id = models.CharField(max_length=50, unique=True)
    
    # Short summary of the bug issue
    subject = models.CharField(max_length=255)
    
    # Detailed description of the bug, including steps to reproduce
    description = models.TextField()
    
    # Current status of the bug in its lifecycle
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    # Importance level of the bug
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Timestamp when the bug was first created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Timestamp of the most recent update to the bug
    updated_at = models.DateTimeField(auto_now=True)
    
    # Counter tracking how many times this bug has been modified
    modified_count = models.IntegerField(default=0)

    def __str__(self):
        """
        String representation of the Bug model.
        
        Returns:
            str: The bug_id, providing a clear identifier when this object is displayed
        """
        return self.bug_id