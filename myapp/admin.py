from django.contrib import admin
from myapp.models import User_master,service_master,cust_master,host_master,contact_master
# Register your models here.
admin.site.register(User_master)
admin.site.register(service_master)
admin.site.register(cust_master)
admin.site.register(host_master)
admin.site.register(contact_master)