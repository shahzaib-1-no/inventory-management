import factory, random
from factory.django import DjangoModelFactory
from faker import Faker
from inventory.models import Supplier, Category, Warehouse, Product
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
import requests

fake = Faker()


def get_user_with_permission(codename=None):
    user = (
        User.objects.filter(groups__permissions__codename=codename)
        .order_by("?")
        .first()
    )
    if not user:
        raise ImproperlyConfigured(f"No user with {codename} permission found")
    return user


# ---------------- Category Factory ---------------
class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    category_name = factory.Faker("word")
    parent_category = None
    is_active = True
    created_by = factory.LazyFunction(get_user_with_permission("add_category"))
    updated_by = factory.SelfAttribute("created_by")
    created_at = factory.Faker("date_time")
    updated_at = factory.Faker("date_time")

    @factory.post_generation
    def sub_categories(self, create, extracted, **kwargs):
        if not create:
            return

        # 1 se 10 tak random subcategories
        total_subs = random.randint(1, 10)
        for i in range(total_subs):
            Category.objects.create(
                category_name=f"{self.category_name}_sub_{i+1}",
                parent_category=self,
                is_active=True,
            )


# ---------------- Warehouse Factory ---------------


class WarehouseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Warehouse

    warehouse_name = factory.Faker("company")
    address = factory.Faker("address")
    city = factory.Faker("city")
    notes = factory.Faker("sentence", nb_words=6)
    is_active = True
    created_at = factory.Faker("date_time")
    updated_at = factory.Faker("date_time")

    created_by = factory.LazyFunction(get_user_with_permission("add_warehouse"))
    updated_by = factory.SelfAttribute("created_by")


# ---------------- Supplier Factory ---------------
class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    supplier_name = factory.Faker("company")
    contact_person = factory.Faker("name")
    phone_number = factory.Faker("phone_number")
    email = factory.Faker("email")
    address = factory.Faker("address", locale="en_US")
    city = factory.Faker("city", locale="en_US")
    opening_balance = factory.Faker("random_int", min=1000, max=10000)
    notes = factory.Faker("sentence", nb_words=6, locale="en_US")
    is_active = True
    payment_terms = factory.Faker(
        "random_element",
        elements=[choice[0] for choice in Supplier.PAYMENT_TERMS_CHOICES],
    )
    created_at = factory.Faker("date_time")
    updated_at = factory.Faker("date_time")

    created_by = factory.LazyFunction(get_user_with_permission("add_supplier"))
    updated_by = factory.SelfAttribute("created_by")


# ---------------- Product Factory ---------------


def get_random_active_subcategory():
    subcats = Category.objects.filter(is_active=True, parent_category__isnull=False)
    return (
        random.choice(subcats)
        if subcats.exists()
        else Category.objects.filter(is_active=True).first()
    )


def get_random_active_supplier():
    suppliers = Supplier.objects.filter(is_active=True)
    return random.choice(suppliers) if suppliers.exists() else Supplier.objects.first()


def get_random_active_warehouse():
    warehouses = Warehouse.objects.filter(is_active=True)
    return (
        random.choice(warehouses) if warehouses.exists() else Warehouse.objects.first()
    )


def random_grocery_image():
    """Download and return a random grocery-style image file."""
    seed = random.randint(1, 9999)
    url = f"https://picsum.photos/seed/{seed}/300"
    response = requests.get(url)
    return ContentFile(response.content, name=f"product_{seed}.jpg")


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    product_name = factory.Faker("word")
    category = factory.LazyFunction(
        lambda: random.choice(Category.objects.filter(is_active=True))
    )
    supplier = factory.LazyFunction(
        lambda: random.choice(Supplier.objects.filter(is_active=True))
    )
    warehouse = factory.LazyFunction(
        lambda: random.choice(Warehouse.objects.filter(is_active=True))
    )
    purchase_price = factory.Faker("random_int", min=1000, max=10000)
    selling_price = factory.Faker("random_int", min=1000, max=10000)
    tax_rate = factory.Faker("random_int", min=1, max=10)
    measure = factory.Faker("word")
    stock = factory.Faker("random_int", min=1, max=10)
    is_active = True
    notes = factory.Faker("sentence", nb_words=6)
    manufacture_date = factory.Faker("date_time")
    expiry_date = factory.Faker("date_time")
    created_by = factory.LazyFunction(lambda: get_user_with_permission("add_product"))
    updated_by = factory.SelfAttribute("created_by")
    created_at = factory.Faker("date_time")
    updated_at = factory.Faker("date_time")

    @factory.post_generation
    def image(self, create, extracted, **kwargs):
        """Attach random image file after creation."""
        if not create:
            return
        image_file = random_grocery_image()
        self.image.save(image_file.name, image_file, save=True)
