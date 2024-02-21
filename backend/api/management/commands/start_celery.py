from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Runs Celery Worker and Beat'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting Celery Worker and Beat...')
        subprocess.Popen(['celery', '-A', 'backend', 'worker', '--loglevel=info'])
        subprocess.Popen(['celery', '-A', 'backend', 'beat', '--loglevel=info'])
