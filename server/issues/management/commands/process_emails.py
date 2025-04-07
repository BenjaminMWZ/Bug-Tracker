import imaplib
import email
from email.header import decode_header
import re
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from issues.models import Bug
import os
import django
import logging

# Load Django settings if running standalone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

# Email configuration
EMAIL_HOST = "imap.gmail.com"  # IMAP server for Gmail
EMAIL_USER = "bugTracker404@gmail.com"  # Email account that receives bug reports
EMAIL_PASSWORD = "jenl qufz avdg crbx"  # App Password for Gmail (more secure than regular password)
MAILBOX = "INBOX"  # Mailbox to check for new emails
BUG_ID_PATTERN = r"Bug ID: (\S+)"  # Regex pattern to extract bug ID from email subjects

# Get a logger for the email processor
logger = logging.getLogger('bug_tracker')

"""Command to fetch and process unread bug report emails from a mailbox."""
class Command(BaseCommand):
    help = "Fetch and process unread bug report emails"

    def handle(self, *args, **kwargs):
        """
        Main function to fetch and process emails.
        
        This is the entry point of the command that:
        1. Connects to the email server
        2. Fetches unread emails
        3. Processes each email to extract bug information
        4. Creates or updates bug records in the database
        5. Marks the emails as read
        6. Logs the results
        """
        self.stdout.write(f"Starting email processing at {now().strftime('%Y-%m-%d %H:%M:%S')}")
        mail = self.connect_to_email()
        if not mail:
            self.stdout.write(self.style.ERROR("Failed to connect to email server."))
            return

        email_ids = self.fetch_unread_emails(mail)
        if not email_ids:
            self.stdout.write(self.style.SUCCESS("No unread emails to process."))
            return

        for email_id in email_ids:
            self.process_email(mail, email_id)

        mail.logout()
        self.stdout.write(self.style.SUCCESS("Successfully processed emails."))
        self.stdout.write(f"Completed email processing at {now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def connect_to_email(self):
        """
        Connect to the email server via IMAP.
        
        Establishes a secure SSL connection to the IMAP server,
        authenticates with the provided credentials, and selects
        the inbox.
        
        Returns:
            imaplib.IMAP4_SSL: Connected IMAP client object, or None if connection fails
        """
        try:
            mail = imaplib.IMAP4_SSL(EMAIL_HOST)
            mail.login(EMAIL_USER, EMAIL_PASSWORD)
            mail.select(MAILBOX)
            return mail
        except Exception as e:
            self.stderr.write(f"Error connecting to email: {e}")
            return None

    def fetch_unread_emails(self, mail):
        """
        Fetch unread emails.
        
        Searches the selected mailbox for unread emails using the UNSEEN flag.
        
        Args:
            mail (imaplib.IMAP4_SSL): Connected IMAP client
            
        Returns:
            list: List of email IDs (as bytes), empty list if none found or error occurs
        """
        try:
            status, messages = mail.search(None, 'UNSEEN')
            if status != "OK":
                return []

            return messages[0].split()
        except Exception as e:
            self.stderr.write(f"Error fetching emails: {e}")
            return []

    def parse_email(self, msg):
        """
        Extract bug ID, subject, and description from an email.
        
        Parses the email message to extract:
        1. Bug ID from the subject line using regex pattern
        2. Subject (with bug ID prefix removed if present)
        3. Description from the message body
        
        If no bug ID is found in the subject, it generates an automatic one.
        
        Args:
            msg (email.message.Message): Email message to parse
            
        Returns:
            tuple: (bug_id, subject, description)
        """
        subject = ""
        description = ""

        # Extract subject from email headers
        if msg["Subject"]:
            subject_bytes, encoding = decode_header(msg["Subject"])[0]
            subject = subject_bytes.decode(encoding or "utf-8") if isinstance(subject_bytes, bytes) else subject_bytes

        # Extract bug ID from subject using regex
        bug_id_match = re.search(BUG_ID_PATTERN, subject)
        bug_id = bug_id_match.group(1) if bug_id_match else None

        # Extract description from message body
        if msg.is_multipart():
            # Handle multipart messages (with attachments)
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                # Only use the plaintext part for description, skip attachments
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    description = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                    break
        else:
            # Handle simple text messages
            description = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8")

        # If no bug_id is found, generate one
        if not bug_id:
            # Generate a unique ID based on timestamp and part of subject
            timestamp = now().strftime("%Y%m%d%H%M%S")
            subject_slug = re.sub(r'[^a-z0-9]', '', subject.lower()[:10])
            bug_id = f"AUTO-{timestamp}-{subject_slug}"
            
        return bug_id, subject, description
        
    def extract_status(self, subject, description):
        """
        Extract bug status from subject and description with improved pattern matching.
        
        Looks for status indicators with various formats:
        - Status: open/closed/etc.
        - State: in progress/etc.
        - [open]/[closed]/etc.
        - "Bug is now closed"/etc.
        
        Args:
            subject (str): Email subject line
            description (str): Email body text
            
        Returns:
            str: Detected status ("open", "closed", "resolved", "in_progress")
                 Default is "open" if no status indicators are found
        """
        # Normalize text for pattern matching
        combined_text = f"{subject} {description}".lower()
        
        # Define status patterns with common prefixes
        status_patterns = [
            # Match formal status indicators like "Status: open"
            r"(?:status|state)\s*:\s*(open|closed|resolved|in[-_\s]progress)",
            # Match bracketed status like "[open]"
            r"\[(open|closed|resolved|in[-_\s]progress)\]",
            # Match status verbs like "closing this bug"
            r"(?:bug|issue|ticket) (?:is|has been|was) (open(?:ed)?|clos(?:ed|ing)|resolv(?:ed|ing)|in[-_\s]progress)",
            # Match direct status mentions
            r"\b(open(?:ed)?|clos(?:ed|ing)|resolv(?:ed|ing)|in[-_\s]progress)\b",
        ]
        
        # Try each pattern
        for pattern in status_patterns:
            match = re.search(pattern, combined_text, re.IGNORECASE)
            if match:
                status_text = match.group(1).lower()
                
                # Normalize various status formats
                if re.match(r"open(?:ed)?", status_text):
                    return "open"
                elif re.match(r"clos(?:ed|ing)", status_text):
                    return "closed"
                elif re.match(r"resolv(?:ed|ing)", status_text):
                    return "resolved"
                elif re.match(r"in[-_\s]progress", status_text):
                    return "in_progress"
        
        # Default status for new bugs
        return "open"

    def determine_priority(self, subject, description):
        """
        Determine priority based on keywords in the email.
        
        Analyzes the email content to detect priority indicators:
        1. Formal notation like "Priority: High"
        2. Keywords like "urgent", "critical", "trivial", etc.
        
        Args:
            subject (str): Email subject line
            description (str): Email body text
            
        Returns:
            str: Detected priority level ("High", "Medium", "Low")
                 Default is "Medium" if no priority indicators are found
        """
        text = f"{subject} {description}".lower()  # Combine and lowercase text

        # Keywords for each priority level
        high_keywords = ["urgent", "high", "critical", "blocker", "emergency", "p1", "priority 1"]
        medium_keywords = ["medium", "normal", "moderate", "p2", "priority 2"]
        low_keywords = ["low", "minor", "trivial", "p3", "priority 3", "can wait"]
        
        # Check for priority indicators with formal notation (e.g., "Priority: High")
        priority_match = re.search(r"priority\s*:\s*(high|medium|low)", text, re.IGNORECASE)
        if priority_match:
            return priority_match.group(1).capitalize()
            
        # Check for keywords
        for keyword in high_keywords:
            if keyword in text:
                return "High"
        
        for keyword in medium_keywords:
            if keyword in text:
                return "Medium"
                
        for keyword in low_keywords:
            if keyword in text:
                return "Low"
                
        # Default to Medium priority
        return "Medium"

    def process_email(self, mail, email_id):
        """
        Process a single email and update/create a Bug record.
        
        This method:
        1. Fetches the full email content
        2. Parses it to extract bug information
        3. Determines status and priority
        4. Creates a new bug or updates an existing one
        5. Marks the email as read
        
        Args:
            mail (imaplib.IMAP4_SSL): Connected IMAP client
            email_id (bytes): ID of the email to process
        """
        try:
            # Fetch the email content
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                logger.error(f"Failed to fetch email {email_id}")
                self.stderr.write(f"Failed to fetch email {email_id}")
                return

            # Parse the email message
            msg = email.message_from_bytes(msg_data[0][1])
            bug_id, subject, description = self.parse_email(msg)

            # Print debug info about extracted data
            self.stdout.write(f"Extracted bug_id: {bug_id} from email with subject: {subject}")

            # Extract status using the improved method
            bug_status = self.extract_status(subject, description)
            
            # Determine priority
            bug_priority = self.determine_priority(subject, description)

            # Log what we're about to do
            logger.info(f"Processing bug ID: {bug_id}, Status: {bug_status}, Priority: {bug_priority}")
            self.stdout.write(f"Processing bug ID: {bug_id}, Status: {bug_status}, Priority: {bug_priority}")

            # Create or update the bug
            bug, created = Bug.objects.get_or_create(
                bug_id=bug_id,
                defaults={
                    "subject": subject,
                    "description": description,
                    "status": bug_status,
                    "priority": bug_priority,
                    "created_at": now(),
                    "updated_at": now(),
                    "modified_count": 0,
                },
            )

            # If the bug already exists, update fields
            if not created:
                # Update everything except the bug_id
                bug.subject = subject
                bug.description = description
                bug.status = bug_status
                bug.priority = bug_priority
                bug.modified_count += 1
                bug.updated_at = now()
                bug.save()
                self.stdout.write(f"Updated Bug: {bug_id} with {bug.modified_count} modification(s).")
            else:
                self.stdout.write(f"Created new Bug: {bug_id}")

            # Mark the email as read to prevent reprocessing
            mail.store(email_id, "+FLAGS", "\\Seen")
            
        except Exception as e:
            logger.error(f"Error processing email {email_id}: {str(e)}")
            self.stderr.write(f"Error processing email {email_id}: {str(e)}")