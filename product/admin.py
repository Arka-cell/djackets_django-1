from django.contrib import admin

from .models import Category, Product, ProductColors
from django.utils.safestring import mark_safe
from django.conf import settings


admin.site.register(Category)
admin.site.register(ProductColors)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("category", "name", "slug", "description", "price", "quantity", "has_colors", "colors")
    readonly_fields = ("colors",)
    def colors(self, obj):
        if obj.has_colors:
            colors = ProductColors.objects.filter(product=obj.id)
            html_div = ""
            for color in colors:
                html_div = html_div + f'''
                                        <div style="width:500px; margin: 0 auto; text-align:center">
                                            Color Name: <a href="http://127.0.0.1:8000/admin/product/productcolors/{color.id}/change/">{color.name}</a>
                                        </div>
                                        '''
            return mark_safe(html_div)
