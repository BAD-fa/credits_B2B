from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

from .managers import CustomUserManager


class User(AbstractUser):
    credit = models.PositiveBigIntegerField(default=0)

    objects = CustomUserManager()

    def add_credit(self, amount: int):
        try:
            self.credit += amount
            self.save()
        except Exception as e:
            raise Exception(f"Can't add this amount to credit because of {e}")

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.password = make_password(self.password)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Supplier(User):
    is_staff = True
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Supplier'


class Customer(User):
    phone_number = models.CharField(max_length=11)

    class Meta:
        verbose_name = 'Customer'


class Operation(models.Model):
    TYPE = [
        ("R", "Received"),
        ("S", "Sent"),
    ]
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="users")
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    type = models.CharField(choices=TYPE, max_length=10)
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, default="Failed")

    def delete(self, using=None, keep_parents=False):
        raise Exception('Operations can not be deleted')

    def save(self, *args, **kwargs):
        if self.pk is None:
            try:
                user = User.objects.select_for_update().get(id=self.user.id)
                with transaction.atomic():
                    user.add_credit(self.amount)
                    self.status = "successful"
                    self.message = f"{self.amount} is {self.type}"
            except Exception as e:
                self.status = e
            finally:
                return super().save(*args, **kwargs)
        else:
            raise Exception('Operations can not be edited')
