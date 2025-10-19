# inventory/management/commands/seed_group.py

from django.core.management.base import BaseCommand
from dashboard.factories import GroupFactory  # agar factory alag file me hai


class Command(BaseCommand):
    help = "Generate fake groups with random permissions"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            type=int,
            default=2,
            help="Number of fake groups to create",
        )

    def handle(self, *args, **options):
        total = options["total"]

        for _ in range(total):
            try:
                group = GroupFactory()
                self.stdout.write(self.style.SUCCESS(f"✅ Created group: {group.name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"💥 Error: {e}"))
