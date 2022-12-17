from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .validators import validate_money


class BankAccount(models.Model):
    account_text = models.CharField(max_length=100)
    creation_date = models.DateTimeField('Date of creation')
    money = models.IntegerField(default=1000, validators=[validate_money])

    def __str__(self):
        return f'''Bank account #{self.pk}
            {self.account_text} 
            ({self.creation_date.strftime("%Y-%m-%d")}) 
            with ${str(self.money)}'''

    def clean(self):
        super().clean()
        # if BankAccount.objects.filter(account_text=self.account_text):
            # raise ValidationError(_('This account already exists!'))

    def can_spend_money(self, asked_money):
        return self.money > 0 and int(asked_money) <= self.money

    def spend_money(self, ticket):
        asked_money = int(ticket.money)
        # if the ticket already exists
        if self.ticket_set.filter(pk=ticket.pk):
            outdated_ticket = self.ticket_set.get(pk=ticket.pk)
            self.restore_money(outdated_ticket)

        if self.can_spend_money(asked_money):
            # avoid race condition via F()
            self.money = F('money') - asked_money
            self.save()
            self.refresh_from_db()


    def restore_money(self, ticket):
        asked_money = int(ticket.money)
        # avoid race condition via F()
        self.money = F('money') + asked_money
        self.save()
        self.refresh_from_db()


class Ticket(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    ticket_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField('Publication date')
    money = models.IntegerField(default=1, validators=[validate_money])

    def __str__(self):
        return f'''<{self.pub_date.strftime("%Y-%m-%d %H:%M:%S")}> 
            #{str(self.pk)} 
            {self.ticket_text} -- ${self.money}'''

    def clean(self):
        super().clean()
        validate_money(int(self.money))
        if not self.account.can_spend_money(self.money):
            raise ValidationError(_('Not enough money on the account balance.'))

    def save(self, *args, **kwargs):
        self.clean()
        self.account.spend_money(self)
        super(Ticket, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.account.restore_money(self)
        super(Ticket, self).delete(*args, **kwargs)



