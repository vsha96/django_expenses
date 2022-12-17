# from slick_reporting.views import SlickReportView
# from slick_reporting.fields import SlickReportField

# from django.db.models import Sum, Avg, Count
# from django.utils.translation import gettext_lazy as _

# from .models import BankAccount, Ticket

# class TotalExpensivePizza(SlickReportView):
#     report_model = Ticket
#     date_field = 'pub_date'

#     group_by = 'ticket_text'

#     columns = [
#         # 'id',
#         'account',
#         'ticket_text',
#         SlickReportField.create(method=Sum, field='money', name='sum_money', verbose_name=_('sum_money')),
#         SlickReportField.create(method=Avg, field='money', name='avg_money', verbose_name=_('average_money_spent')),
#         SlickReportField.create(method=Count, field='money', name='count_act', verbose_name=_('total_actions')),
#     ]

#     charts_settings = [
#      {
#         'type': 'bar',
#         'data_source': 'value__sum',
#         'title_source': 'title',
#      },
#     ]