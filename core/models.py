from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name

class EntryBaseModel(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Expense(EntryBaseModel):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    last_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='last_updated_by')
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_by')
    included_users = models.ManyToManyField(User, related_name='included_users')


    def split_equally(self):
        """
        Split the expense equally among the included users.
        """
        equal_amount = self.amount / self.included_users.count()
        expense_splits = [] # List of ExpenseSplit objects

        for user in self.included_users.all():
            expense_splits.append(ExpenseSplit(
                expense=self,
                user=user,
                amount=equal_amount
            ))

        ExpenseSplit.objects.bulk_create(expense_splits)

    def split_by_percentage(self, split_data):
        """
        Handles splitting by amount or equally.
        Args:
            split_data (list of dict or None): A list of dictionaries with user and amount.
                Example:
                    [
                        {"user_id": 1, "amount": 500.0},
                        {"user_id": 2, "amount": 500.0}
                    ]
                If None, split equally among included users.
        """

        included_users = self.included_users.all()

        if split_data:
            # Validate the provided amounts
            total_amount = sum([item['amount'] for item in split_data])
            if total_amount != self.amount:
                raise ValueError("The total split amounts must equal the expense amount.")

            # Create splits based on provided amounts
            for item in split_data:
                user = User.objects.get(id=item['user_id'])
                ExpenseSplit.objects.create(
                    expense=self,
                    user=user,
                    amount=item['amount']
                )
        else:
            # Split equally if no amounts are provided
            equal_amount = self.amount / included_users.count()
            for user in included_users:
                ExpenseSplit.objects.create(
                    expense=self,
                    user=user,
                    amount=equal_amount
                )

class Group(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(User, related_name='members')
    expenses = models.ManyToManyField(Expense, related_name='expenses')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by', null=True, blank=True)

    def __str__(self):
        return self.name

    def add_expense(self, expense: Expense):
        self.expenses.add(expense)
        self.save()

class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='splits')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
