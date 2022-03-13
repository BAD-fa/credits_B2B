from django.contrib import admin

from .models import User, Customer, Supplier, Operation


class CreditDataAdmin(admin.ModelAdmin):
    readonly_fields=('credit',)



admin.site.register(Supplier,CreditDataAdmin)
admin.site.register(Customer,CreditDataAdmin)


class SuperUserAdmin(CreditDataAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_superuser=True)


admin.site.register(User,SuperUserAdmin)


class OperationAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return Operation.objects.filter(user=request.user.id)


admin.site.register(Operation,OperationAdmin)




