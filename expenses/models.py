from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class GeneralObject(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    modify_date = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.create_date = datetime.datetime.today()
        return super(GeneralObject, self).save(*args, **kwargs)


class IconClass(GeneralObject):
    name = models.CharField(max_length=150)
    icon = models.CharField(max_length=150)
    def __unicode__(self):
        return self.name

def content_file_path(instance, filename):
    return '/'.join([str(instance.user.id), filename])


class Attachment(GeneralObject):
    user = models.ForeignKey(User, null=True)
    file = models.FileField(upload_to=content_file_path)

    def __unicode__(self):
        return self.user.username + " " + self.file.name


class Category(GeneralObject):
    name = models.CharField(max_length=500)
    icon_class = models.ForeignKey(IconClass)
    user = models.ForeignKey(User, null=True)
    def __unicode__(self):
        return self.name


class SubCategory(GeneralObject):
    name = models.CharField(max_length=500)
    category = models.ForeignKey(Category)
    icon_class = models.ForeignKey(IconClass)
    user = models.ForeignKey(User, null=True)
    income = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Account(GeneralObject):
    name = models.CharField(max_length=500)
    icon_class = models.ForeignKey(IconClass)
    month_balance = models.FloatField(null=False, default=0)
    user = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.name


class PaymentType(GeneralObject):
    name = models.CharField(max_length=500)
    icon_class = models.ForeignKey(IconClass)
    account = models.ForeignKey(Account)

    def __unicode__(self):
        return self.name


class Transaction(GeneralObject):
    sub_category = models.ForeignKey(SubCategory)
    amount = models.FloatField(default=0)
    account = models.ForeignKey(Account, editable=False, default=None)
    payment_type = models.ForeignKey(PaymentType)
    comment = models.CharField(max_length=500, null=True)
    attachment = models.ForeignKey(Attachment, null=True)
    tran_date = models.DateField('Transaction Date', default=datetime.date.today)
    paid = models.BooleanField(default=False)
    income = models.BooleanField(default=False)
    parent_transaction = models.ForeignKey('self', null=True, default=None)
    recurrent_date = models.DateField('Reccurent Date', null=True, default=None)

    def save(self, *args, **kwargs):
        ''' On save, update account '''
        self.account = self.payment_type.account
        # if not self.id and self.income:
        #     self.amount -= self.amount
        return super(Transaction, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.comment


def calculate_transaction(account, transaction, reverse=False):
    amount = transaction.amount
    if transaction.income:
        amount = -amount
    if reverse:
        amount = -amount
    account.month_balance -= amount


def calculate_balance(account):
    transactions = Transaction.objects.filter(tran_date__lte=datetime.date.today, paid=False)
    for transaction in transactions:
        calculate_transaction(account, transaction)
        #transaction.paid = True
    transactions.update(paid=True)
    account.save()