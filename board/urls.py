from django.urls import path
from .views import (HomePageView, ItemList, ItemDetail, ItemDetailNonAccess, ItemCreate, ItemEdit, ItemDelete,
                    ReplyList, MySalesList,
                    MyPurchasesList,
                    accept_reply, delete_reply, reject_reply, ReplyEdit, mail_code)

urlpatterns = [
    path('', HomePageView.as_view(), name="home_page"),
    path('verify/', mail_code, name="verify_account"),
    path('list/', ItemList.as_view(), name='item_list'),
    path('my_sales/', MySalesList.as_view(), name='my_sales_list'),
    path('my_purchases/', MyPurchasesList.as_view(), name='my_purchases_list'),
    path('<int:pk>', ItemDetail.as_view(), name='item_detail'),
    path('none/<int:pk>', ItemDetailNonAccess.as_view(), name='item_detail_non_access'),
    path('create/', ItemCreate.as_view(), name='item_create'),
    path('<int:pk>/edit/', ItemEdit.as_view(), name='item_edit'),
    path('<int:pk>/delete/', ItemDelete.as_view(), name='item_delete'),
    path('reply/', ReplyList.as_view(), name='reply_list'),
    path('reply/<int:pk>/accept/', accept_reply, name='accept_reply'),
    path('reply/<int:pk>/delete/', delete_reply, name='delete_reply'),
    path('reply/<int:pk>/reject/', reject_reply, name='reject_reply'),
    path('<int:pk>/edit_reply/', ReplyEdit.as_view(), name='reply_edit'),
]