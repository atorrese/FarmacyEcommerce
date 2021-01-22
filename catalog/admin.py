from django.contrib import admin
from .models import Product,Category,Presentation,Mark, Images
from import_export import  resources
from import_export.admin import  ImportExportModelAdmin


# Category
class CategoryResource(resources.ModelResource):
    class Meta:
        model =Category

class CategoryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','get_icon',)
    resource_class = CategoryResource
# Mark
class MarkResource(resources.ModelResource):
    class Meta:
        model =Mark

class MarkAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','get_icon',)
    resource_class = MarkResource
# Presentation
class PresentationResource(resources.ModelResource):
    class Meta:
        model =Presentation

class PresentationAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name',)
    resource_class = MarkResource

# Product        
class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ProductImageInline(admin.TabularInline):
    model= Images
    extra=3
    

class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['name','description','price',]
    list_display = ('name','description','presentation','category','mark','price','stock','elaboration_date','expiration_date','get_image',)
    inlines= [ProductImageInline,]
    resource_class = ProductResource

"""     def get_category(self,obj):
        return  "\n".join([c.Name for c in obj.CategoryId.all()]) """

admin.site.register(Category,CategoryAdmin)
admin.site.register(Presentation,PresentationAdmin)
admin.site.register(Mark,MarkAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images)