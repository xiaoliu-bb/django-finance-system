from rest_framework import serializers
from .models import (
    JournalEntry,
    JournalItem,
    Invoice,
    AccountCategory,
    Budget,
    BudgetItem
)

# 账户分类序列化器
class AccountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountCategory
        fields = '__all__'

# 日记账项目序列化器
class JournalItemSerializer(serializers.ModelSerializer):
    account = AccountCategorySerializer(read_only=True)
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=AccountCategory.objects.all(),
        source='account',
        write_only=True
    )

    class Meta:
        model = JournalItem
        fields = '__all__'

# 日记账序列化器
class JournalEntrySerializer(serializers.ModelSerializer):
    items = JournalItemSerializer(many=True, required=False)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = JournalEntry
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        entry = JournalEntry.objects.create(**validated_data)

        for item_data in items_data:
            JournalItem.objects.create(entry=entry, **item_data)

        return entry

# 发票序列化器
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

# 预算序列化器
class BudgetSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    approved_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ('created_at', 'approved_at')

# 预算项序列化器
class BudgetItemSerializer(serializers.ModelSerializer):
    account = AccountCategorySerializer(read_only=True)
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=AccountCategory.objects.all(),
        source='account',
        write_only=True
    )

    class Meta:
        model = BudgetItem
        fields = '__all__'