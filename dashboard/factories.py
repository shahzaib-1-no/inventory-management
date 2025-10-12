import random
import factory
from faker import Faker
from dashboard.forms import (
    RegisterForm,
)
from django.contrib.auth.models import User, Group


fake = Faker()


# ---------------- RegisterForm Factory ---------------
class RegisterFormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}_{fake.user_name()}")
    email = factory.Sequence(lambda n: f"user_{n}_{fake.email()}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "password123")
    is_staff = False
    is_active = True

    @factory.post_generation
    def assign_role(obj, create, extracted, **kwargs):
        """Assign random role to user"""
        if not create:
            # Object not saved yet — skip
            return

        # Agar koi specific role pass kiya gaya hai (e.g. extracted)
        if extracted:
            obj.groups.add(extracted)
        else:
            # Random group assign kar do
            groups = list(Group.objects.all())
            if groups:
                obj.groups.add(fake.random_element(groups))
