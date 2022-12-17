from .models import BankAccount, Ticket

from rest_framework import serializers


class BankAccountSerializer(serializers.ModelSerializer):
    queryset = BankAccount.objects.order_by('-creation_date')
    class Meta:
        model = BankAccount
        fields = ['pk', 'account_text', 'creation_date', 'money']


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    # account = serializers.SerializerMethodField()
    # account = BankAccountSerializer()
    account = serializers.PrimaryKeyRelatedField(queryset=BankAccount.objects.all())
    # account.queryset = BankAccount.objects.all()

    class Meta:
        model = Ticket
        fields = ['pk', 'account', 'ticket_text', 'pub_date', 'money']

    
    # def get_account(self, ticket) -> int:
    #     return ticket.account.pk