from django.core.management.base import BaseCommand
import subprocess
import os
import signal
import sys

class Command(BaseCommand):
    """
    Custom Django management command that runs Django server, Celery worker,
    and Celery beat concurrently in a single terminal session.
    """
    help = 'Runs the server with Celery worker and beat'

    def handle(self, *args, **options):
        """
        Main command handler that starts all required processes and manages their lifecycle.
        
        Starts three processes:
        1. Django development server
        2. Celery worker for processing asynchronous tasks
        3. Celery beat for scheduled tasks
        
        Handles graceful termination when receiving keyboard interrupt (Ctrl+C).
        
        Args:
            *args: Variable length argument list
            **options: Arbitrary keyword arguments from command line
        """
        self.stdout.write('Starting Django server, Celery worker, and Celery beat')
        
        processes = []  # List to keep track of all started subprocesses
        try:
            # Start Django development server
            self.stdout.write("Starting Django server...")
            django_process = subprocess.Popen(['python', 'manage.py', 'runserver'])
            processes.append(django_process)
            
            # Start Celery worker for processing asynchronous tasks (e.g. email processing)
            self.stdout.write("Starting Celery worker...")
            worker_process = subprocess.Popen(['celery', '-A', 'server', 'worker', '--loglevel=info'])
            processes.append(worker_process)
            
            # Start Celery beat for scheduled periodic tasks
            self.stdout.write("Starting Celery beat scheduler...")
            beat_process = subprocess.Popen(['celery', '-A', 'server', 'beat', '--loglevel=info'])
            processes.append(beat_process)
            
            # Wait for processes to complete (they typically run until terminated)
            # This keeps the command running and output visible
            for process in processes:
                process.wait()
                
        except KeyboardInterrupt:
            # Handle clean shutdown when user presses Ctrl+C
            self.stdout.write("Shutting down all processes...")
            
            # Terminate each process with SIGTERM signal
            for process in processes:
                os.kill(process.pid, signal.SIGTERM)
                
            # Exit the command cleanly
            self.stdout.write("All processes terminated successfully")
            sys.exit(0)