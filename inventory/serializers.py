from rest_framework import serializers
from .models import Product, StockTransaction, StockDetail

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class StockDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockDetail
        fields = ['product', 'quantity']

class StockTransactionSerializer(serializers.ModelSerializer):
    details = StockDetailSerializer(many=True, write_only=True)
    detail_records = StockDetailSerializer(source='stockdetail_set', many=True, read_only=True)


    class Meta:
        model = StockTransaction
        fields = ['id', 'type', 'timestamp', 'details','detail_records']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        transaction = StockTransaction.objects.create(**validated_data)
        for detail in details_data:
            StockDetail.objects.create(transaction=transaction, **detail)
        return transaction
