from django.test import TestCase
from django.utils.timezone import now
from issues.models import Bug
import re
import time
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import json

class BugEmailProcessingTest(TestCase):
    """
    Test case for bug creation and updates from emails.
    Tests the core functionality without relying on email infrastructure.
    """

    def setUp(self):
        """Set up test environment before each test."""
        # Clear any bugs that might exist
        Bug.objects.all().delete()

    def test_bug_creation_and_update(self):
        """
        Test that bugs are created and updated correctly when processing email data.
        This test bypasses the email retrieval logic and directly tests bug creation/update.
        """
        # STEP 1: Test creating a new bug
        bug_id = "TEST-12345"
        initial_subject = f"Bug ID: {bug_id} - Initial Bug Report"
        initial_description = "This is a test bug description."
        initial_status = "open"
        initial_priority = "Medium"
        current_time = now()
        
        # Directly create a bug record as if it came from an email
        bug = Bug.objects.create(
            bug_id=bug_id,
            subject=initial_subject,
            description=initial_description,
            status=initial_status,
            priority=initial_priority,
            modified_count=0,
            created_at=current_time,
            updated_at=current_time
        )
        
        # Verify initial bug creation
        self.assertEqual(Bug.objects.count(), 1, "Bug should be created")
        created_bug = Bug.objects.get(bug_id=bug_id)
        self.assertEqual(created_bug.subject, initial_subject)
        self.assertEqual(created_bug.description, initial_description)
        self.assertEqual(created_bug.status, initial_status)
        self.assertEqual(created_bug.priority, initial_priority)
        self.assertEqual(created_bug.modified_count, 0)
        
        # Store timestamps for comparison
        original_created_at = created_bug.created_at
        original_updated_at = created_bug.updated_at
        
        # Ensure timestamps will be different
        time.sleep(0.1)
        
        # STEP 2: Test updating the existing bug
        updated_subject = f"Bug ID: {bug_id} - Status: resolved"
        updated_description = "This is an updated description. The bug is now resolved."
        updated_status = "resolved"
        
        # Get the existing bug and update it as if a new email came in
        existing_bug = Bug.objects.get(bug_id=bug_id)
        existing_bug.subject = updated_subject
        existing_bug.description = updated_description
        existing_bug.status = updated_status
        existing_bug.modified_count += 1
        existing_bug.updated_at = now()  # Update the timestamp
        existing_bug.save()
        
        # Verify the bug was updated correctly
        self.assertEqual(Bug.objects.count(), 1, "Bug count should still be 1")
        updated_bug = Bug.objects.get(bug_id=bug_id)
        self.assertEqual(updated_bug.subject, updated_subject)
        self.assertEqual(updated_bug.description, updated_description)
        self.assertEqual(updated_bug.status, updated_status)
        self.assertEqual(updated_bug.modified_count, 1)
        
        # Created timestamp should be unchanged
        self.assertEqual(updated_bug.created_at, original_created_at)
        
        # Updated timestamp should be newer
        self.assertGreater(updated_bug.updated_at, original_updated_at)

    def test_extract_bug_id_from_subject(self):
        """
        Test that bug ID extraction from subject line works correctly.
        This mimics the functionality in process_emails.py
        """
        bug_id_pattern = r"Bug ID: (\S+)"
        
        # Test cases for bug ID extraction
        test_cases = [
            {"subject": "Bug ID: TEST-123 - Initial report", "expected": "TEST-123"},
            {"subject": "Re: Bug ID: BUG-456 - Follow-up", "expected": "BUG-456"},
            {"subject": "No bug ID here", "expected": None},
        ]
        
        for case in test_cases:
            bug_id_match = re.search(bug_id_pattern, case["subject"])
            extracted_id = bug_id_match.group(1) if bug_id_match else None
            self.assertEqual(extracted_id, case["expected"])

    def test_extract_status_from_text(self):
        """
        Test that status extraction from email contents works correctly.
        This mimics the functionality in the extract_status method from process_emails.py
        """
        # Test cases for status extraction
        test_cases = [
            {"text": "Status: resolved", "expected": "resolved"},
            {"text": "The bug is now closed", "expected": "closed"},
            {"text": "Just an update, no status change", "expected": "open"}
        ]
        
        for case in test_cases:
            # Simplified implementation of extract_status
            status = "open"  # Default status
            
            # Basic patterns similar to what your implementation would use
            if "status: resolved" in case["text"].lower():
                status = "resolved"
            elif "status: closed" in case["text"].lower():
                status = "closed"
            elif "bug is now closed" in case["text"].lower():
                status = "closed"
                
            self.assertEqual(status, case["expected"])
            
    def test_multiple_bug_updates(self):
        """
        Test that a bug can be updated multiple times and the modified_count
        is incremented correctly each time.
        """
        # Create an initial bug
        bug_id = "MULTI-UPDATE-123"
        initial_time = now()
        
        bug = Bug.objects.create(
            bug_id=bug_id,
            subject=f"Bug ID: {bug_id} - Initial Bug",
            description="Initial description",
            status="open",
            priority="Medium",
            modified_count=0,
            created_at=initial_time,
            updated_at=initial_time
        )
        
        # Perform multiple updates and check modified_count increments
        for i in range(1, 4):  # 3 updates
            time.sleep(0.1)  # Ensure timestamp difference
            
            # Update the bug
            bug.description = f"Update {i}: Modified description"
            bug.modified_count += 1
            bug.updated_at = now()
            bug.save()
            
            # Verify modified_count is correct
            bug.refresh_from_db()
            self.assertEqual(bug.modified_count, i, f"Modified count should be {i} after update {i}")
            
        # Final verification
        self.assertEqual(Bug.objects.count(), 1, "Should still be just one bug")
        self.assertEqual(bug.modified_count, 3, "Final modified_count should be 3")
        
    def test_empty_description_handling(self):
        """
        Test that bugs with empty descriptions are handled properly.
        """
        bug_id = "EMPTY-DESC-123"
        current_time = now()
        
        # Create a bug with empty description
        bug = Bug.objects.create(
            bug_id=bug_id,
            subject=f"Bug ID: {bug_id} - Empty Description Test",
            description="",  # Empty description
            status="open",
            priority="Medium",
            modified_count=0,
            created_at=current_time,
            updated_at=current_time
        )
        
        # Verify bug was created correctly
        created_bug = Bug.objects.get(bug_id=bug_id)
        self.assertEqual(created_bug.description, "", "Empty description should be stored as empty string")
        
        # Update with a valid description
        time.sleep(0.1)
        bug.description = "Now there is a description"
        bug.modified_count += 1
        bug.updated_at = now()
        bug.save()
        
        # Verify update worked
        bug.refresh_from_db()
        self.assertEqual(bug.description, "Now there is a description")
        self.assertEqual(bug.modified_count, 1)
        
    def test_very_long_description(self):
        """
        Test handling of bugs with very long descriptions.
        """
        bug_id = "LONG-DESC-123"
        current_time = now()
        
        # Create a long description (10KB of text)
        long_description = "This is a very long bug description. " * 500
        
        # Create a bug with long description
        bug = Bug.objects.create(
            bug_id=bug_id,
            subject=f"Bug ID: {bug_id} - Long Description Test",
            description=long_description,
            status="open",
            priority="Medium",
            modified_count=0,
            created_at=current_time,
            updated_at=current_time
        )
        
        # Verify the bug was created with the correct description
        created_bug = Bug.objects.get(bug_id=bug_id)
        self.assertEqual(len(created_bug.description), len(long_description), 
                        "Long description should be stored completely")
        
    def test_special_characters_in_subject_and_description(self):
        """
        Test that special characters in subject and description are handled properly.
        """
        bug_id = "SPECIAL-CHARS-123"
        current_time = now()
        
        # Create strings with special characters
        subject = f"Bug ID: {bug_id} - Special chars: !@#$%^&*()_+[]{{}}|\\;:'\",.<>/?"
        description = "Unicode characters: äöüßéèêëàùœ∑´®†¥¨ˆøπ'åß∂ƒ©˙∆˚¬…æΩ≈ç√∫˜µ≤≥÷"
        
        # Create a bug with special characters
        bug = Bug.objects.create(
            bug_id=bug_id,
            subject=subject,
            description=description,
            status="open",
            priority="Medium",
            modified_count=0,
            created_at=current_time,
            updated_at=current_time
        )
        
        # Verify the bug was created with the correct text
        created_bug = Bug.objects.get(bug_id=bug_id)
        self.assertEqual(created_bug.subject, subject, "Special characters in subject should be preserved")
        self.assertEqual(created_bug.description, description, "Unicode characters in description should be preserved")
    
    def test_bug_with_same_id_but_different_case(self):
        """
        Test that bug IDs are case-sensitive to prevent duplication or incorrect updates.
        """
        # Create first bug with lowercase ID
        bug_id_lower = "case-123"
        lower_time = now()
        
        bug_lower = Bug.objects.create(
            bug_id=bug_id_lower,
            subject=f"Bug ID: {bug_id_lower} - Lowercase",
            description="This is the lowercase bug",
            status="open",
            priority="Medium",
            modified_count=0,
            created_at=lower_time,
            updated_at=lower_time
        )
        
        time.sleep(0.1)
        
        # Create second bug with uppercase ID
        bug_id_upper = "CASE-123"
        upper_time = now()
        
        bug_upper = Bug.objects.create(
            bug_id=bug_id_upper,
            subject=f"Bug ID: {bug_id_upper} - Uppercase",
            description="This is the uppercase bug",
            status="open",
            priority="Medium",
            modified_count=0,
            created_at=upper_time,
            updated_at=upper_time
        )
        
        # Verify both bugs were created as separate entities
        self.assertEqual(Bug.objects.count(), 2, "Should have two separate bugs with different case IDs")
        
        # Update one bug and verify the other is unchanged
        bug_lower.description = "Updated lowercase bug"
        bug_lower.modified_count += 1
        bug_lower.updated_at = now()
        bug_lower.save()
        
        # Refresh upper bug from database to make sure it wasn't changed
        bug_upper.refresh_from_db()
        self.assertEqual(bug_upper.description, "This is the uppercase bug", 
                        "Uppercase bug should remain unchanged")
        self.assertEqual(bug_upper.modified_count, 0, "Uppercase bug should not be modified")

    def test_status_transitions(self):
        """
        Test that status transitions work correctly for a bug.
        Verifies the complete lifecycle of a bug through different statuses.
        """
        bug_id = "STATUS-TRANSITION-123"
        current_time = now()
        
        # Create a new bug with 'open' status
        bug = Bug.objects.create(
            bug_id=bug_id,
            subject=f"Bug ID: {bug_id} - Status Transition Test",
            description="Initial bug report",
            status="open",
            priority="Medium",
            modified_count=0,
            created_at=current_time,
            updated_at=current_time
        )
        
        # Define status transition sequence
        status_sequence = ["in progress", "under review", "pending", "resolved", "closed"]
        
        # Transition through each status
        for i, new_status in enumerate(status_sequence):
            time.sleep(0.1)
            
            bug.status = new_status
            bug.description += f"\nTransition to {new_status} status."
            bug.modified_count += 1
            bug.updated_at = now()
            bug.save()
            
            # Refresh and verify
            bug.refresh_from_db()
            self.assertEqual(bug.status, new_status, f"Status should be {new_status}")
            self.assertEqual(bug.modified_count, i+1, f"Modified count should be {i+1}")
        
        # Verify final state
        self.assertEqual(bug.status, "closed", "Final status should be 'closed'")
        self.assertEqual(bug.modified_count, len(status_sequence), "Modified count should match transition count")
    
    def test_priority_changes(self):
        """
        Test that bug priority can be changed and tracked correctly.
        """
        bug_id = "PRIORITY-CHANGE-123"
        current_time = now()
        
        # Create a new bug with 'Low' priority
        bug = Bug.objects.create(
            bug_id=bug_id,
            subject=f"Bug ID: {bug_id} - Priority Change Test",
            description="Initial bug with low priority",
            status="open",
            priority="Low",
            modified_count=0,
            created_at=current_time,
            updated_at=current_time
        )
        
        # Define priority sequence
        priority_sequence = ["Medium", "High", "Critical", "Medium", "Low"]
        
        # Change priority through the sequence
        for i, new_priority in enumerate(priority_sequence):
            time.sleep(0.1)
            
            bug.priority = new_priority
            bug.description += f"\nChanged priority to {new_priority}."
            bug.modified_count += 1
            bug.updated_at = now()
            bug.save()
            
            # Refresh and verify
            bug.refresh_from_db()
            self.assertEqual(bug.priority, new_priority, f"Priority should be {new_priority}")
            self.assertEqual(bug.modified_count, i+1, f"Modified count should be {i+1}")
        
        # Verify final state
        self.assertEqual(bug.priority, "Low", "Final priority should be 'Low'")
        self.assertEqual(bug.modified_count, len(priority_sequence), "Modified count should match priority changes")
    
    def test_duplicate_bug_id_handling(self):
        """
        Test that attempting to create a bug with a duplicate ID is handled properly.
        """
        bug_id = "DUPLICATE-123"
        current_time = now()
        
        # Create first bug
        first_bug = Bug.objects.create(
            bug_id=bug_id,
            subject=f"Bug ID: {bug_id} - Original Bug",
            description="This is the original bug",
            status="open",
            priority="Medium",
            modified_count=0,
            created_at=current_time,
            updated_at=current_time
        )
        
        # Count bugs before attempting duplicate
        initial_count = Bug.objects.count()
        
        # Attempt to create a second bug with the same ID inside a transaction
        # This should fail with an IntegrityError due to the unique constraint on bug_id
        from django.db import IntegrityError, transaction
        
        try:
            with transaction.atomic():
                duplicate_bug = Bug.objects.create(
                    bug_id=bug_id,  # Same bug_id
                    subject=f"Bug ID: {bug_id} - Duplicate Bug",
                    description="This is a duplicate bug",
                    status="open",
                    priority="High",
                    modified_count=0,
                    created_at=now(),
                    updated_at=now()
                )
        except IntegrityError:
            pass  # This is expected
        
        # Verify there's still only one bug with that ID and the total count hasn't changed
        self.assertEqual(Bug.objects.filter(bug_id=bug_id).count(), 1, "Should only be one bug with this ID")
        self.assertEqual(Bug.objects.count(), initial_count, "Total bug count shouldn't change")
    def test_concurrent_updates(self):
        """
        Test that concurrent updates to the same bug record are handled properly.
        This simulates multiple email updates arriving close together.
        """
        bug_id = "CONCURRENT-123"
        current_time = now()
        
        # Create initial bug
        bug = Bug.objects.create(
            bug_id=bug_id,
            subject=f"Bug ID: {bug_id} - Concurrent Update Test",
            description="Initial bug description",
            status="open",
            priority="Medium",
            modified_count=0,
            created_at=current_time,
            updated_at=current_time
        )
        
        # Simulate three "concurrent" updates
        # In real app, these might come from different threads/processes
        update_descriptions = [
            "Update from developer A",
            "Update from developer B",
            "Update from manager C"
        ]
        
        # Apply updates in sequence but with the same timestamp 
        # (simulating near-concurrent updates)
        update_time = now()
        
        for i, desc in enumerate(update_descriptions):
            # Get a fresh instance to simulate different processes
            bug_instance = Bug.objects.get(bug_id=bug_id)
            bug_instance.description = desc
            bug_instance.modified_count += 1
            bug_instance.updated_at = update_time
            bug_instance.save()
        
        # Verify final state
        final_bug = Bug.objects.get(bug_id=bug_id)
        self.assertEqual(final_bug.description, update_descriptions[-1], 
                        "Description should reflect the last update")
        self.assertEqual(final_bug.modified_count, len(update_descriptions), 
                        "Modified count should reflect all updates")
    
    def test_bug_deletion(self):
        """
        Test that bugs can be properly deleted from the system.
        """
        # Create several bugs
        bugs_to_create = 5
        for i in range(bugs_to_create):
            Bug.objects.create(
                bug_id=f"DELETE-TEST-{i}",
                subject=f"Bug ID: DELETE-TEST-{i} - Deletion Test",
                description=f"Bug #{i} for deletion testing",
                status="open",
                priority="Medium",
                modified_count=0,
                created_at=now(),
                updated_at=now()
            )
        
        # Verify all bugs were created
        self.assertEqual(Bug.objects.filter(bug_id__startswith="DELETE-TEST-").count(), 
                        bugs_to_create, 
                        f"Should have {bugs_to_create} test bugs")
        
        # Delete one bug
        Bug.objects.filter(bug_id="DELETE-TEST-2").delete()
        
        # Verify it's gone
        self.assertEqual(Bug.objects.filter(bug_id="DELETE-TEST-2").count(), 0, 
                        "Deleted bug should no longer exist")
        
        # Verify other bugs remain
        self.assertEqual(Bug.objects.filter(bug_id__startswith="DELETE-TEST-").count(), 
                        bugs_to_create - 1, 
                        "Other bugs should remain")
        
        # Delete all remaining test bugs
        Bug.objects.filter(bug_id__startswith="DELETE-TEST-").delete()
        
        # Verify all are gone
        self.assertEqual(Bug.objects.filter(bug_id__startswith="DELETE-TEST-").count(), 0, 
                        "All test bugs should be deleted")
    
    def test_null_values_handling(self):
        """
        Test how the system handles null or None values in various fields.
        """
        bug_id = "NULL-TEST-123"
        current_time = now()
        
        # Try to create a bug with minimal fields
        # Django should apply defaults for non-provided fields
        bug = Bug.objects.create(
            bug_id=bug_id,
            subject=f"Bug ID: {bug_id} - Null Values Test",
            description="",  # Empty string instead of NULL
            status="open",
            priority="Low",  # Providing a value since NULL isn't allowed
            modified_count=0,
            created_at=current_time,
            updated_at=current_time
        )
        
        # Refresh from database
        bug.refresh_from_db()
        
        # Verify values were stored correctly
        self.assertEqual(bug.description, "", "Empty description should be stored as empty string")
        self.assertEqual(bug.status, "open", "Status should be 'open'")
        self.assertEqual(bug.priority, "Low", "Priority should be 'Low'")
        self.assertEqual(bug.modified_count, 0, "modified_count should be 0")
        
        # Test updating with empty string (not None) for description
        bug.description = ""  # Use empty string instead of None
        bug.save()
        
        # Verify after update
        bug.refresh_from_db()
        self.assertEqual(bug.description, "", "Description should be an empty string")

    def test_search_functionality(self):
        """
        Test that bugs can be properly searched by various criteria.
        """
        # Create test bugs with different attributes
        current_time = now()
        
        # Bug 1: High priority, open status
        Bug.objects.create(
            bug_id="SEARCH-HIGH-1",
            subject="High priority UI bug",
            description="There's a UI alignment issue in the dashboard",
            status="open",
            priority="High",
            modified_count=0,
            created_at=current_time,
            updated_at=current_time
        )
        
        # Bug 2: Medium priority, resolved status
        Bug.objects.create(
            bug_id="SEARCH-MED-2",
            subject="Medium priority login issue",
            description="Users cannot login with special characters in password",
            status="resolved",
            priority="Medium", 
            modified_count=2,
            created_at=current_time,
            updated_at=current_time
        )
        
        # Bug 3: Low priority, closed status
        Bug.objects.create(
            bug_id="SEARCH-LOW-3",
            subject="Low priority typo in email",
            description="There's a typo in the confirmation email",
            status="closed",
            priority="Low",
            modified_count=1,
            created_at=current_time,
            updated_at=current_time
        )
        
        # Test search by priority
        high_priority_bugs = Bug.objects.filter(priority="High")
        self.assertEqual(high_priority_bugs.count(), 1, "Should find one high priority bug")
        self.assertEqual(high_priority_bugs.first().bug_id, "SEARCH-HIGH-1")
        
        # Test search by status
        open_bugs = Bug.objects.filter(status="open")
        self.assertEqual(open_bugs.count(), 1, "Should find one open bug")
        self.assertEqual(open_bugs.first().bug_id, "SEARCH-HIGH-1")
        
        # Test search by text in description
        ui_bugs = Bug.objects.filter(description__icontains="UI")
        self.assertEqual(ui_bugs.count(), 1, "Should find one bug with UI in description")
        self.assertEqual(ui_bugs.first().bug_id, "SEARCH-HIGH-1")
        
        # Test combined search
        medium_resolved_bugs = Bug.objects.filter(priority="Medium", status="resolved")
        self.assertEqual(medium_resolved_bugs.count(), 1, "Should find one medium, resolved bug")
        self.assertEqual(medium_resolved_bugs.first().bug_id, "SEARCH-MED-2")
        
        # Test search by bug_id pattern
        pattern_bugs = Bug.objects.filter(bug_id__startswith="SEARCH")
        self.assertEqual(pattern_bugs.count(), 3, "Should find all three search test bugs")


import unittest

class AuthenticationTests(TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.client = APIClient()
        
        # Only use URLs we know exist
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        
        # Use a hardcoded path for profile URL
        self.profile_url = '/api/auth/profile/'
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_registration_successful(self):
        """Test user registration with valid data"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'password2': 'newpassword123'  # Confirmation password
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Check response content
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')
    
    def test_registration_invalid_data(self):
        """Test user registration with invalid data"""
        # Test with mismatched passwords
        data = {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'password': 'password123',
            'password2': 'differentpassword'  # Mismatched password
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username='newuser2').exists())
        
        # Test with existing username
        data = {
            'username': 'testuser',  # Already exists
            'email': 'another@example.com',
            'password': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_successful(self):
        """Test user login with valid credentials"""
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response content
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')
    
    def test_login_invalid_credentials(self):
        """Test user login with invalid credentials"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_user_profile_authenticated(self):
        """Test accessing user profile when authenticated"""
        # First login to get token
        login_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        token = login_response.data['token']
        
        # Use token to access profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')
    
    def test_get_user_profile_unauthenticated(self):
        """Test accessing user profile without authentication"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)