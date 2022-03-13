from django.contrib.auth.models import Group, Permission

def create_supplier_group():
    new_group, created = Group.objects.get_or_create(name='suppliers')



    add_operation_per = Permission.objects.get(codename="add_operation")
    view_operation_per = Permission.objects.get(codename="view_operation")
    new_group.permissions.add(add_operation_per)
    new_group.permissions.add(view_operation_per)
