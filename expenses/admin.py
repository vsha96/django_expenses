from django.contrib import admin
from django.views import View
from django.shortcuts import render

from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect

from .models import BankAccount, Ticket

import logging
logger_db = logging.getLogger('django.db.backends')


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 3


class TicketAdmin(admin.ModelAdmin):
    search_fields = ['ticket_text', 'money']

    list_display = ('account', 'ticket_text', 'pub_date', 'money')
    list_filter = ['account', 'money']

    list_per_page = 10


class BankAccountAdmin(admin.ModelAdmin):
    search_fields = ['account_text']

    list_display = ('account_text', 'creation_date', 'money')
    list_filter = ['creation_date']

    fieldsets = [
        (None, {'fields': ['account_text', 'money']}),
        ('Date Information', 
            {'fields': ['creation_date']
            ,'classes': ['collapse']}),
    ]

    inlines = [TicketInline]


# ==================
# ===CUSTOM ADMIN===
# ==================

# uncomment it to get back to the default admin
# there are also in settings.py and urls.py
# admin.site.register(BankAccount, BankAccountAdmin)
# admin.site.register(Ticket, TicketAdmin)

from django.contrib.auth.models import User
from django.test.client import RequestFactory

class CustomAdminSite(admin.AdminSite):
    site_header = "Custom Admin by vsha96"
    site_title  = "Custom Admin by vsha96"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('report/',
                self.admin_view((
                CustomAdminReport.as_view(admin_site=self))), name='report'),
        ]
        return my_urls + urls


admin_reports = CustomAdminSite(name='admin_report')

admin_reports.register(BankAccount, BankAccountAdmin)
admin_reports.register(Ticket, TicketAdmin)



# from django.contrib.auth.models import User
# from django.test.client import RequestFactory

# req = RequestFactory().get('/admin/')
# req.user = User.objects.get(username='admin')
# av_apps = admin.site.each_context(req)['available_apps']

# print("### MOVING ADMIN APPS TO CUSTOM ADMIN ###")
# print(admin.site)
# print(admin.site.each_context(req))
# req = RequestFactory().get('/admin/')
# req.user = User.objects.get(username='admin')
# av_apps = admin.site.each_context(req)['available_apps']
# for app in av_apps:
#     for m in app['models']:
#         # admin_reports.register(m['model'])
        # print(f"# register: {m['model']}")



from .forms import ReportByTextByMoney
from django.db.models import Sum, Count
import time

class CustomAdminReport(View):
    admin_site = admin_reports

    def get(self, request):
        report_form = ReportByTextByMoney()
        return render(request, 'admin/report.html', {
            'form': report_form,
            'error_message': '',
        })

    def post(self, request):
        ticket_text = str(request.POST['ticket_text'])
        money = int(request.POST['money'])
        init_data = {'ticket_text': ticket_text, 'money': money}

        report_form = ReportByTextByMoney(init_data)

        report_result_list = [['id', 'account_text', 'ticket_text', 'total_money_spent', 'total_actions']]

        try:
            start_time = time.time()
            logger_db.info("#########################")
            logger_db.info("MAKING REPORT")

            for acc in BankAccount.objects.all().order_by('id'):
                account_text = acc.account_text
                acc_ticket_set = acc.ticket_set.all()
                total_money_spent = None
                total_actions = None
                if acc_ticket_set.exists():
                    tickets_filtered = acc_ticket_set.filter(ticket_text__startswith=ticket_text).filter(money=money)
                    if tickets_filtered.exists():
                        ticket_text = tickets_filtered[0].ticket_text
                        total_money_spent = list(tickets_filtered.aggregate(Sum('money')).values())[0]
                        total_actions = list(tickets_filtered.aggregate(Count('money')).values())[0]

                report_result_list.append([acc.id, account_text, ticket_text, total_money_spent, total_actions])

            end_time = time.time()
            total_time = end_time - start_time

            report_result_list.append(["Execution time:", f"{total_time * 1000} ms"])

            logger_db.info("END REPORT")
            logger_db.info("#########################")

        except Exception as err:
            
            return render(request, 'admin/report.html', {
                'form': report_form,
                'report_result_list': report_result_list,
                'error_message': err,
            })
        else:

            return render(request, 'admin/report.html', {
                'form': report_form,
                'report_result_list': report_result_list,
            })


