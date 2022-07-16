from django.contrib import admin

from motivator.models import Goal, Payment, Refund

# Register your models here.
admin.site.register(Goal)
admin.site.register(Payment)
admin.site.register(Refund)
