from django.contrib import admin

from .models import User, Customer, Supplier, Operation


admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Operation)
