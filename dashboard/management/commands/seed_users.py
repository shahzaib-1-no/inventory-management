from dashboard.factories import RegisterFormFactory
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    """
    Django custom command to generate fake users for testing or demo purpose.
    Usage:
        python manage.py seed_users <total>
    Example:
        python manage.py seed_users 10
    """

    help = "Generate fake users using factory_boy and Faker."

    def add_arguments(self, parser):
        parser.add_argument(
            "total",
            type=int,
            help="Number of fake users to create",
        )

    def handle(self, *args, **options):
        total = options["total"]

        # Ensure at least one group exists
        if not Group.objects.exists():
            self.stdout.write(
                self.style.WARNING("⚠️ No Groups found. Please create roles first.")
            )
            return

        # Generate fake users
        try:
            for _ in range(total):
                user = RegisterFormFactory.create()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"💥 Error: {e}"))
            return

        self.stdout.write(
            self.style.SUCCESS(f"🎉 Successfully created {total} fake users!")
        )
