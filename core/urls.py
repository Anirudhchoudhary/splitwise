from django.urls import path
from .views import HomeView, ModalTestView, CreateGroupView, GroupDetailsView, CreateExpenseView, ExpenseDetailsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('modal/test/', ModalTestView.as_view(), name='modal_test'),
    path('create_group/', CreateGroupView.as_view(), name='create_group'),
    path('group_details/<int:pk>/', GroupDetailsView.as_view(), name='group_details'),
    path('create_expense/', CreateExpenseView.as_view(), name='create_expense'),
    path('expense_details/<int:pk>/', ExpenseDetailsView.as_view(), name='expense_details'),
]
