from django.core.management.base import BaseCommand
from inventory.factories import SupplierFactory
from django.core.exceptions import ImproperlyConfigured


class Command(BaseCommand):
    help = "Generate fake suppliers using factory_boy and Faker."

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            type=int,
            default=5,
            help="Number of fake suppliers to create",
        )

    def handle(self, *args, **options):
        total = options["total"]

        try:
            for _ in range(total):
                supplier = SupplierFactory.create()
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Created supplier: {supplier.supplier_name}")
                )
        except ImproperlyConfigured as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"💥 Unexpected Error: {e}"))
            return

        self.stdout.write(
            self.style.SUCCESS(f"🎉 Successfully created {total} fake suppliers!")
        )
