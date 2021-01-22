from django.contrib import admin
from import_export import  resources
from import_export.admin import  ImportExportModelAdmin

from .models import Order, OrderDetail, Client

# Category
class ClientResource(resources.ModelResource):
    class Meta:
        model =Client

class ClientAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['user']
    list_display = ('get_first_name','get_last_name','get_email','address',)

    resource_class = ClientResource

    def get_first_name(self, obj):
 
        return obj.user.first_name

    get_first_name.short_description = 'Nombres'
    get_first_name.admin_order_field = 'user__first_name'
    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.short_description = 'Apellidos'
    get_last_name.admin_order_field = 'user__last_name'

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'

class OrderResource(resources.ModelResource):
    class Meta:
        model =Order

class DetailOrderInline(admin.TabularInline):
    model= OrderDetail
    extra=1


class OrderAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['client']
    list_display = ('client','type_pay','paid','paypal_id',)
    inlines=  [DetailOrderInline,]
    resources= OrderResource

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderDetail)
admin.site.register(Client,ClientAdmin)
