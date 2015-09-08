from expenses.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    icon_class = serializers.ReadOnlyField(source='icon_class.icon')
    class Meta:
        model = Category
        fields = ('id', 'name', 'icon_class', 'user')
        read_only_fields = ('user', )


class SubCategorySerializer(serializers.ModelSerializer):
    icon = serializers.ReadOnlyField(source='icon_class.icon')
    parent_icon = serializers.ReadOnlyField(source='category.icon_class.icon')
    category = serializers.ReadOnlyField(source='category.name')
    user = serializers.ReadOnlyField(source='user.username')


    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'category', 'icon', 'parent_icon', 'user')
        read_only_fields = ('user', )


class IconClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = IconClass
        fields = ('id', 'name', 'icon')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'icon_class', 'month_balance', 'user')
        read_only_fields = ('user', )


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ('id', 'name', 'icon_class', 'account', )


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'sub_category', 'amount', 'payment_type', 'comment', 'attachment', 'tran_date', 'account')
        read_only_fields = ('account', )


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'user', 'file', )