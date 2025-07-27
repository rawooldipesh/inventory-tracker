from django.urls import path
from .views import ProductListView, StockSummaryView, StockTransactionCreateView, InventoryStatusView, stock_history_page, stock_summary_page

urlpatterns = [
    path('', stock_summary_page, name='home'),
    path('products/', ProductListView.as_view()),
    path('transactions/', StockTransactionCreateView.as_view()),
    path('inventory/', InventoryStatusView.as_view()),
    path('stock-summary/', StockSummaryView.as_view(), name='stock-summary'),
    path('stock-summary-ui/', stock_summary_page, name='stock-summary-ui'),
    path('stock-history/', stock_history_page, name='stock-history'),

]
