import imaplib
import email
from email.header import decode_header
import re
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from issues.models import Bug
import os
import django

# Load Django settings if running standalone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

# Email configuration
EMAIL_HOST = "imap.gmail.com"
EMAIL_USER = "bugTracker404@gmail.com"
EMAIL_PASSWORD = "jenl qufz avdg crbx"  # Use an App Password for security
MAILBOX = "INBOX"
BUG_ID_PATTERN = r"Bug ID: (\S+)"

"""Command to fetch and process unread bug report emails from a mailbox."""
class Command(BaseCommand):
    help = "Fetch and process unread bug report emails"

    def handle(self, *args, **kwargs):
        """Main function to fetch and process emails."""
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

    def connect_to_email(self):
        """Connect to the email server via IMAP."""
        try:
            mail = imaplib.IMAP4_SSL(EMAIL_HOST)
            mail.login(EMAIL_USER, EMAIL_PASSWORD)
            mail.select(MAILBOX)
            return mail
        except Exception as e:
            self.stderr.write(f"Error connecting to email: {e}")
            return None

    def fetch_unread_emails(self, mail):
        """Fetch unread emails."""
        try:
            status, messages = mail.search(None, 'UNSEEN')
            if status != "OK":
                return []

            return messages[0].split()
        except Exception as e:
            self.stderr.write(f"Error fetching emails: {e}")
            return []

    def parse_email(self, msg):
        """Extract bug ID, subject, and description from an email."""
        subject = ""
        description = ""

        if msg["Subject"]:
            subject_bytes, encoding = decode_header(msg["Subject"])[0]
            subject = subject_bytes.decode(encoding or "utf-8") if isinstance(subject_bytes, bytes) else subject_bytes

        bug_id_match = re.search(BUG_ID_PATTERN, subject)
        bug_id = bug_id_match.group(1) if bug_id_match else None

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    description = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                    break
        else:
            description = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8")

        return bug_id, subject, description

    
    def process_email(self, mail, email_id):
        """Process a single email and update/create a Bug record."""
        try:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                self.stderr.write(f"Failed to fetch email {email_id}")
                return

            msg = email.message_from_bytes(msg_data[0][1])
            bug_id, subject, description = self.parse_email(msg)

            # Parse the subject to get the status('open', 'in_progress', 'resolved', 'closed')
            # If subject contains 'xxx', set status to 'xxx'
            status_match = re.search(r"\b(open|in_progress|resolved|closed)\b", subject, re.IGNORECASE)
            if status_match:
                bug_status = status_match.group(1).lower()
            else:
                bug_status = "open"

            # If no bug_id is found, skip the email
            if not bug_id:
                self.stderr.write(f"Skipping email {email_id}: No Bug ID found.")
                return

            def determine_priority(subject, description):
                """Determine priority based on keywords in the email."""
                text = f"{subject} {description}".lower()  # Combine and lowercase text

                if "urgent" in text or "high" in text:
                    return "High"
                elif "medium" in text:
                    return "Medium"
                elif "low" in text or "minor" in text:
                    return "Low"
                else:
                    return "Medium"  # Default priority

            bug_priority = determine_priority(subject, description)  

            # Include created_at and updated_at in defaults
            bug, created = Bug.objects.get_or_create(
                bug_id=bug_id,
                defaults={
                    "subject": subject,
                    "description": description,
                    "status": "open",
                    "priority": bug_priority,
                    "created_at": now(),  # Set created_at to the current timestamp
                    "updated_at": now(),  # Set updated_at to the current timestamp
                    "modified_count": 0,
                },
            )

            # If the bug already exists, update the description or priority if needed
            if not created:
                # Update everything except the bug_id
                bug.subject = subject
                bug.description = description
                bug.priority = bug_priority
                bug.status = bug_status
                bug.modified_count += 1
                bug.updated_at = now()
                bug.save()
                self.stdout.write(f"Updated Bug: {bug_id} with {bug.modified_count} modification(s).")
            else:
                self.stdout.write(f"Created new Bug: {bug_id}")

            mail.store(email_id, "+FLAGS", "\\Seen")
            
        except Exception as e:
            self.stderr.write(f"Error processing email {email_id}: {e}")
            return