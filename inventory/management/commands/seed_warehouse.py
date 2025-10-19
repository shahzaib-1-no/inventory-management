from django.core.management.base import BaseCommand
from inventory.factories import WarehouseFactory


class Command(BaseCommand):
    help = "Generate fake warehouses using factory_boy and Faker."

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            type=int,
            default=2,
            help="Number of fake warehouses to create",
        )

    def handle(self, *args, **options):
        total = options["total"]

        try:
            for _ in range(total):
                WarehouseFactory.create()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"💥 Error: {e}"))
            return

        self.stdout.write(
            self.style.SUCCESS(f"🎉 Successfully created {total} fake warehouses!")
        )
