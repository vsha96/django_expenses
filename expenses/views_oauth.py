from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.utils import timezone

from .models import BankAccount
from .forms import AccountForm


def create_account_oauth(backend, user, response, *args, **kwargs):
    # print("\n===AAAAA===\n")
    # print(response['display_name'] + '::' + response['email'])
    # print('\n\n')

    if backend.name == 'twitch':
        try:
            new_account = BankAccount()
            new_account.account_text = response['display_name'] + '::' + response['email']
            new_account.creation_date = timezone.now()
            new_account.money = new_account.money # default value
            new_account.clean()
        except ValidationError as err:
            # Redisplay the account creation form.
            prev_data = {'account_text': new_account.account_text}
            del(new_account)
            account_form = AccountForm(initial=prev_data)
            account_form.fields['money'].disabled = True
            return render(None, 'expenses/add_account.html', {
                'error_message': err.message,
                'form': account_form
            })
        else:
            new_account.save()
            return HttpResponseRedirect(reverse('expenses:index'))

    return HttpResponseRedirect(reverse('expenses:index'))

