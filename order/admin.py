from django.contrib import admin

from .models import Order, OrderItem, PersonalInfos
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


admin.site.register(OrderItem)


@admin.register(PersonalInfos)
class PersonalInfosAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "created_at", "user_id")
    readonly_fields = ("user_id",)
    def user_id(self, obj):
        if obj.user:
            return obj.user.id


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user',)
    readonly_fields = ('products', 'total_price')

    def products(self, obj):
        if obj.id:
            order_items = OrderItem.objects.filter(order=obj.id)
            products = [order_item.product for order_item in order_items]
            html_div = ""
            for product in products:
                html_div = html_div + f'''
                                        <div style="width:500px; margin: 0 auto; text-align:center">
                                            <strong><h3 style="text-align:center"><a href="http://127.0.0.1:8000/admin/product/product/{product.id}/change/">See {product.name}</a></h3></strong>
                                            <h3 style="text-align:center"><strong>Product description:<br></strong></h3><div style="margin: 0 auto"><div>{product.description}</div></div>
                                            <h3 style="text-align:center"><strong>Stock Quantity</strong></h3> <p style="text-align: center">{product.quantity}</p>
                                            <img src="{product.image.url}" style="width: 300px; display:block;margin:auto">
                                            <br>
                                            <hr>
                                            <br>
                                            <br>
                                        </div>
                                        '''
            return mark_safe(html_div)
        return None
    

    def total_price(self, obj):
        if obj:
            order_items = OrderItem.objects.filter(order=obj.id)
            total = sum([product.price for product in order_items])
            return mark_safe(total)
