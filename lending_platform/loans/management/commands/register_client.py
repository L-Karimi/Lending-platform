from django.core.management.base import BaseCommand
from loans.services import ScoringService
from loans.models import ClientRegistration

class Command(BaseCommand):
    help = 'Register this service with the Scoring Engine'
    

    def handle(self, *args, **options):
        if ClientRegistration.objects.exists():
            self.stdout.write(self.style.WARNING(
                "Client is already registered with Scoring Engine"
            ))
            return
            
        self.stdout.write("Registering client with Scoring Engine...")
        client = ScoringService.register_client()
        
        if client:
            self.stdout.write(self.style.SUCCESS(
                f"Successfully registered client with token: {client.token}"
            ))
            self.stdout.write(self.style.SUCCESS(
                f"Client ID: {client.client_id}"
            ))
        else:
            self.stdout.write(self.style.ERROR(
                "Failed to register client with Scoring Engine"
            ))