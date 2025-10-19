from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from dashboard.factories import RegisterFormFactory


class Command(BaseCommand):
    help = "Generate fake users using factory_boy and Faker."

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            type=int,
            default=2,
            help="Number of fake users to create",
        )

    def handle(self, *args, **options):
        total = options["total"]

        if not Group.objects.exists():
            self.stdout.write(
                self.style.WARNING("⚠️ No Groups found. Please create roles first.")
            )
            return

        for _ in range(total):
            try:
                user = RegisterFormFactory.create()
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Created user: {user.username}")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"💥 Error: {e}"))
                return

        self.stdout.write(
            self.style.SUCCESS(f"🎉 Successfully created {total} fake users!")
        )
