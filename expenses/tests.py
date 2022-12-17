from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.http import HttpRequest

from django.test import Client
client = Client()


from .models import BankAccount, Ticket
from .views import send_money_done


class SendMoneyViewTest(TestCase):
    def setUp(self):
        acc1 = BankAccount.objects.create(
            account_text="acc1", 
            creation_date = timezone.now(),
            money=100,
        )
        acc2 = BankAccount.objects.create(
            account_text="acc2", 
            creation_date = timezone.now(),
            money=100,
        )


    def test_transfer_money_success(self):
        acc1 = BankAccount.objects.get(account_text="acc1")
        acc2 = BankAccount.objects.get(account_text="acc2")
        old_acc1 = acc1
        old_acc2 = acc2

        url = reverse('expenses:send_money_done', args=(acc1.pk,), )
        expected_url = reverse('expenses:index')

        transfer_sum = 10
        data = {
            'money': transfer_sum,
            'recipient_account': acc2.id,
        }

        # print('Test money transfer with success')
        response = self.client.post(url, data, follow=True)

        acc1 = BankAccount.objects.get(account_text="acc1")
        acc2 = BankAccount.objects.get(account_text="acc2")

        self.assertRedirects(response, expected_url)
        self.assertEqual(acc1.money, old_acc1.money - transfer_sum)
        self.assertEqual(acc2.money, old_acc2.money + transfer_sum)
        # print('\t\tOK')


    def test_transfer_money_failed(self):
        acc1 = BankAccount.objects.get(account_text="acc1")
        acc2 = BankAccount.objects.get(account_text="acc2")
        old_acc1 = acc1
        old_acc2 = acc2

        url = reverse('expenses:send_money_done', args=(acc1.pk,), )
        expected_url = reverse('expenses:send_money_done', args=(acc1.pk,),)
        transfer_sum = acc1.money * 10 # more than on the account
        data = {
            'money': transfer_sum,
            'recipient_account': acc2.id,
        }

        # print('Test money transfer with fail')
        response = self.client.post(url, data, follow=True)
        
        acc1 = BankAccount.objects.get(account_text="acc1")
        acc2 = BankAccount.objects.get(account_text="acc2")
        
        self.assertEqual(acc1.money, old_acc1.money)
        self.assertEqual(acc2.money, old_acc2.money)
        
        # print('\t\tOK')





