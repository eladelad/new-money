from django.contrib import admin

# Register your models here.
from expenses.models import *

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(PaymentType)
admin.site.register(IconClass)
admin.site.register(Attachment)