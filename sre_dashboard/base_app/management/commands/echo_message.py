from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Echo test message"

    def handle(self, *args, **options):
        log_entry = "Hello world from app"
        self.stdout.write(log_entry)

if __name__ == "__main__":
    pass