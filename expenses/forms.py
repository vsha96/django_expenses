from django import forms

from .models import Ticket, BankAccount


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_text', 'money']


class AccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_text', 'money']


class SendMoneyForm(forms.Form):
    sender_account = forms.ModelChoiceField(queryset=BankAccount.objects.all())
    sender_account.disabled = True
    money = forms.IntegerField(min_value=0)
    recipient_account = forms.ModelChoiceField(queryset=BankAccount.objects.order_by('-creation_date'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sender_account = kwargs['initial']['sender_account']

        # exclude sender's account from the list of recipients
        all_acc_without_sender = BankAccount.objects.order_by('-creation_date').exclude(pk=sender_account.pk)
        self.fields['recipient_account'].queryset = all_acc_without_sender


# form for custom admin reporting
class ReportByTextByMoney(forms.Form):
    ticket_text = forms.CharField()
    money = forms.IntegerField(min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if kwargs:
            init_text  = kwargs['initial']['ticket_text']
            init_money = kwargs['initial']['money']
            self.fields['ticket_text'] = init_text
            self.fields['money'] = init_money



    