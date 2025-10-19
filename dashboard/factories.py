import random

import factory
from django.contrib.auth.models import Group, User, Permission
from faker import Faker


fake = Faker()


# ---------------- RegisterForm Factory ---------------
CODE_NAMES = ["add_product", "change_product"]


class RegisterFormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}_{fake.user_name()}")
    email = factory.Sequence(lambda n: f"user_{n}_{fake.email()}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "12345")
    is_staff = False
    is_active = True

    @factory.post_generation
    def assign_role(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.groups.add(extracted)
        else:
            # Filter groups with supplier-related permissions
            groups = Group.objects.filter(
                permissions__codename__in=CODE_NAMES
            ).distinct()
            if groups.exists():
                self.groups.add(groups.order_by("?").first())
            else:
                print(
                    f"⚠️ No eligible group with supplier permissions found for user {self.username}"
                )


# ---------------- Group Factory ---------------
MODELS = ["User", "Supplier", "Category", "Warehouse", "Product"]


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group
        django_get_or_create = ("name",)

    name = factory.LazyFunction(
        lambda: f"role_{random.randint(1000,9999)}_{fake.word()}"
    )

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return
        model = random.choice(MODELS).lower()
        perms = Permission.objects.filter(
            codename__in=[f"add_{model}", f"change_{model}"]
        )
        self.permissions.set(perms)
