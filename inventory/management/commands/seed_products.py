from django.core.management.base import BaseCommand
from django.core.exceptions import ImproperlyConfigured
from inventory.factories import ProductFactory  # adjust path accordingly


class Command(BaseCommand):
    help = "Generate fake products using factory_boy and Faker."

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            type=int,
            default=10,
            help="Number of fake products to create",
        )

    def handle(self, *args, **options):
        total = options["total"]
        created = 0

        self.stdout.write(self.style.NOTICE(f"🚀 Creating {total} fake products..."))

        try:
            for _ in range(total):
                product = ProductFactory.create()
                created += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Created product: {product.product_name}")
                )

        except ImproperlyConfigured as e:
            self.stdout.write(self.style.ERROR(f"❌ Config Error: {e}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"💥 Unexpected Error: {e}"))
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"🎉 Successfully created {created}/{total} fake products!"
            )
        )
