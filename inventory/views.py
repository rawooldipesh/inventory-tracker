from pyexpat.errors import messages
from rest_framework import generics
from .models import Product, StockTransaction
from .serializers import ProductSerializer, StockTransactionSerializer
from django.db.models import Sum, F, Case, When, IntegerField
from rest_framework.response import Response
from rest_framework.views import APIView
from inventory.models import Product, StockDetail
from django.shortcuts import render,redirect



class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class StockTransactionCreateView(generics.CreateAPIView):
    serializer_class = StockTransactionSerializer

class InventoryStatusView(APIView):
    def get(self, request):
        from .models import StockDetail
        from .models import StockTransaction
        inventory = {}
        details = StockDetail.objects.select_related('transaction', 'product')

        for detail in details:
            prod = detail.product.name
            qty = detail.quantity
            if detail.transaction.type == 'IN':
                inventory[prod] = inventory.get(prod, 0) + qty
            else:
                inventory[prod] = inventory.get(prod, 0) - qty

        return Response(inventory)

class StockSummaryView(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = []

        for product in products:
            in_qty = StockDetail.objects.filter(product=product, transaction__type="IN").aggregate(total=Sum('quantity'))['total'] or 0
            out_qty = StockDetail.objects.filter(product=product, transaction__type="OUT").aggregate(total=Sum('quantity'))['total'] or 0
            stock = in_qty - out_qty

            data.append({
                "id": product.id,
                "name": product.name,
                "stock": stock
            })

        return Response(data)


from .models import Product, StockTransaction, StockDetail
from django.utils import timezone
from django.shortcuts import render, redirect

from django.db.models import Sum, Case, When, IntegerField

def stock_summary_page(request):
    if request.method == 'POST':
        product_id = int(request.POST['product_id'])
        quantity = int(request.POST['quantity'])
        movement_type = request.POST['movement_type']

        product = Product.objects.get(id=product_id)

        # Validate for OUT movement
        # Calculate current stock
        in_qty = StockDetail.objects.filter(product=product, transaction__type='IN').aggregate(total=Sum('quantity'))['total'] or 0
        out_qty = StockDetail.objects.filter(product=product, transaction__type='OUT').aggregate(total=Sum('quantity'))['total'] or 0
        current_stock = in_qty - out_qty

        if movement_type == 'OUT' and quantity > current_stock:
            messages.error(request, 'Not enough stock to perform this operation.')
            return redirect('stock-summary-ui')

        # Save transaction
        transaction = StockTransaction.objects.create(type=movement_type)
        StockDetail.objects.create(transaction=transaction, product=product, quantity=quantity)
        return redirect('stock-summary-ui')

    # For GET: calculate stock per product
    products = Product.objects.all()
    stock_data = []
    for p in products:
        in_qty = StockDetail.objects.filter(product=p, transaction__type='IN').aggregate(total=Sum('quantity'))['total'] or 0
        out_qty = StockDetail.objects.filter(product=p, transaction__type='OUT').aggregate(total=Sum('quantity'))['total'] or 0
        current_stock = in_qty - out_qty
        stock_data.append({
            'name': p.name,
            'id': p.id,
            'stock': current_stock
        })

    return render(request, 'inventory/stock_summary.html', {'stock': stock_data,'products':Product.objects.all()})

def stock_history_page(request):
    details = StockDetail.objects.select_related('transaction', 'product').order_by('-transaction__timestamp')
    return render(request, 'inventory/stock_history.html', {'details': details})
