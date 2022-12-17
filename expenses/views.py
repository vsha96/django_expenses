from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.views import generic
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import BankAccount, Ticket
from .forms import TicketForm, AccountForm, SendMoneyForm



import logging
logger = logging.getLogger(__name__)
logger_db = logging.getLogger('django.db.backends')

logger_list = [logger, logger_db]

def all_loggers_info(msg):
    for log in logger_list:
        log.info(msg)

def all_loggers_error(msg):
    for log in logger_list:
        log.error(msg)



class IndexView(generic.ListView):
    template_name = 'expenses/index.html'
    context_object_name = 'bank_account_list'

    def get_queryset(self):
        """Return all bank accounts ordered by creation date."""
        return BankAccount.objects.order_by('-creation_date')

# class AccountDetailView(generic.DetailView):
#     model = BankAccount
#     template_name = 'expenses/account_index.html'


def account_detail(request, account_id):
    account = get_object_or_404(BankAccount, pk=account_id)
    ticket_list = account.ticket_set.order_by('-pub_date')

    return render(
        request,
        'expenses/account_index.html', 
        {'account': account
            ,'ticket_list': ticket_list})


def add_ticket(request, account_id):
    account = get_object_or_404(BankAccount, pk=account_id)
    ticket_form = TicketForm()
    return render(
        request, 
        'expenses/add_ticket.html',
        {'account': account,
        'form': ticket_form})


def create_ticket(request, account_id):
    account = get_object_or_404(BankAccount, pk=account_id)
    try:
        new_ticket = Ticket()
        new_ticket.account = account
        new_ticket.ticket_text = request.POST['ticket_text']
        new_ticket.pub_date = timezone.now()
        new_ticket.money = request.POST['money']
        new_ticket.clean()

    except ValidationError as err:
        prev_data = {'ticket_text': new_ticket.ticket_text}
        ticket_form = TicketForm(initial=prev_data)

        del(new_ticket)

        # Redisplay the ticket creation form.

        return render(request, 'expenses/add_ticket.html', {
            'account': account,
            'error_message': err.message,
            'form': ticket_form
        })
    else:
        new_ticket.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('expenses:detail', args=(account.id,)))

    # return HttpResponse('Created a ticket!')


def add_account(request):
    account_form = AccountForm()
    account_form.fields['money'].disabled = True
    return render(
        request, 
        'expenses/add_account.html',
        {'form': account_form})


def create_account(request):
    try:
        new_account = BankAccount()
        new_account.account_text = request.POST['account_text']
        new_account.creation_date = timezone.now()
        new_account.money = new_account.money # default value
        new_account.clean()
    except ValidationError as err:
        del(new_account)
        # Redisplay the account creation form.
        account_form = AccountForm()
        return render(request, 'expenses/add_account.html', {
            'error_message': err.message,
            'form': account_form
        })
    else:
        new_account.save()
        return HttpResponseRedirect(reverse('expenses:index'))


def send_money(request, account_id):
    sender_account = get_object_or_404(BankAccount, pk=account_id)

    init_data = {'sender_account': sender_account}
    send_money_form = SendMoneyForm(initial=init_data)

    return render(
        request, 
        'expenses/send_money.html',
        {'account': sender_account,
        'form': send_money_form})


@transaction.atomic
def send_money_done(request, account_id):
    sender_account = get_object_or_404(BankAccount, pk=account_id)
    money = int(request.POST['money'])
    recipient_account_pk = request.POST['recipient_account']
    recipient_account = get_object_or_404(BankAccount, pk=recipient_account_pk)
    try:
        # logger.info(f"try to transfer money ${money}")
        # logger.info(f"from <{sender_account.account_text}>")
        # logger.info(f"to <{recipient_account.account_text}>")
        all_loggers_info(f"################################")
        all_loggers_info(f"try to transfer money ${money}")
        all_loggers_info(f"from <{sender_account.account_text}>")
        all_loggers_info(f"to <{recipient_account.account_text}>")


        # transaction savepoint
        tid = transaction.savepoint()

        # do transaction operations
        new_ticket = Ticket()
        new_ticket.account = sender_account
        new_ticket.ticket_text = 'sending money to acc #' + str(recipient_account_pk)
        new_ticket.pub_date = timezone.now()
        new_ticket.money = money
        new_ticket.save()

        if (sender_account.money < 0):
            raise ValidationError(_('Not enough money!'))

        recipient_account.money += money
        recipient_account.save()

    except ValidationError as err:
        # rollback to the transaction savepoint
        transaction.savepoint_rollback(tid)

        # logger.error("money transfer: FAILED (not enough money)")
        all_loggers_error("money transfer: FAILED (not enough money)")
        all_loggers_info(f"################################")

        # rerender form
        init_data = {'sender_account': sender_account}
        send_money_form = SendMoneyForm(initial=init_data)
        return render(request, 'expenses/send_money.html', {
            'account': sender_account,
            'error_message': err.message,
            'form': send_money_form
        })
    else:
        # logger.info(f"money transfer: SUCCEED")
        all_loggers_info(f"money transfer: SUCCEED")
        all_loggers_info(f"################################")

        return HttpResponseRedirect(reverse('expenses:index'))
        # return HttpResponseRedirect(reverse('expenses:detail', args=(account_id,)))







