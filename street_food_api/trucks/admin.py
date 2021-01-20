from django.contrib import admin

from .models import PaymentMethod, Truck, TruckImage


class TruckImageInline(admin.TabularInline):
    model = TruckImage
    fields = ("image",)


class TruckAdmin(admin.ModelAdmin):
    inlines = (TruckImageInline,)


admin.site.register(Truck, TruckAdmin)
admin.site.register(PaymentMethod)
admin.site.register(TruckImage)
