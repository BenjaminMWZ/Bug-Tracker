from django.core.management.base import BaseCommand
import subprocess
import os
import signal
import sys

class Command(BaseCommand):
    help = 'Runs the server with Celery worker and beat'

    def handle(self, *args, **options):
        self.stdout.write('Starting Django server, Celery worker, and Celery beat')
        
        processes = []
        try:
            # Start Django server
            django_process = subprocess.Popen(['python', 'manage.py', 'runserver'])
            processes.append(django_process)
            
            # Start Celery worker
            worker_process = subprocess.Popen(['celery', '-A', 'server', 'worker', '--loglevel=info'])
            processes.append(worker_process)
            
            # Start Celery beat
            beat_process = subprocess.Popen(['celery', '-A', 'server', 'beat', '--loglevel=info'])
            processes.append(beat_process)
            
            # Wait for processes to complete
            for process in processes:
                process.wait()
                
        except KeyboardInterrupt:
            for process in processes:
                os.kill(process.pid, signal.SIGTERM)
            sys.exit(0)