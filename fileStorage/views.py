import redis
import json
import pickle
import weasyprint
from django.shortcuts import render, get_object_or_404, reverse, redirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View
from django.conf import settings
from company.models import Company, BillTitle
from .bill_session import BillSession
from django.http import JsonResponse
from essentials.topological_sort import TopologicalSort, Graph
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from .models import FileStorage
from django.template.loader import render_to_string
from essentials.views import AddDefaultData
from django.conf import settings



r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class BillForm(View):

    def get(self, request, pk, slug):
        company = get_object_or_404(Company, slug=slug, pk=pk)
        invoice_no = company.invoice_no + 1
        list_title = []
        initials = {}
        if company.active:
            bill_title = BillTitle.objects.filter(company=company, active=True)
            name = "company::expressions"
            key = "{}::{}".format(slug, pk)
            for bill in bill_title.iterator():
                if bill.title1:
                    list_title.append(bill.title1)
                if bill.title2:
                    list_title.append(bill.title2)
                if bill.title3:
                    list_title.append(bill.title3)
                if bill.title4:
                    list_title.append(bill.title4)
                if bill.title5:
                    list_title.append(bill.title5)
            if r.hexists(name, key):
                final_list = []
                exp_dict = r.hget(name, key)
                try:
                    exp_dict = pickle.loads(exp_dict)
                    print(exp_dict)
                    g = Graph(len(exp_dict))

                    x_count = 0
                    for x in exp_dict.values():
                        y_count = 0
                        for y in exp_dict.keys():
                            if x.count('{'+y+'}') > 0:
                                print(x, y)
                                g.addEdge(y_count, x_count, x)
                                print(y_count, x_count, x)
                            y_count += 1
                        x_count += 1
                    t = TopologicalSort(g)

                    topological_list = t.topological_sort()
                    print(t.topological_sort())
                    for i in topological_list:
                        final_list.append(list_title[i])
                    print(final_list)
                    graph = json.dumps(g.dict)
                    print(graph)
                    search_field = ""
                    if r.hexists(name="company::search_fields", key="{}::{}".format(slug, pk)):
                        search_field = r.hget(name="company::search_fields", key="{}::{}".format(slug, pk))
                        search_field = search_field.decode()
                        print(search_field)
                    return render(request, 'bill.html', {'bill_title': final_list, 'table_list': list_title,
                                                         'invoice_no': invoice_no, 'graph': graph, 'is_exp':'true',
                                                         "search_field": search_field, 'pk': pk, 'slug': slug})
                except pickle.UnpicklingError as e:
                    print(e)
                    pass
            return render(request, 'bill.html', {'bill_title': list_title, 'table_list': list_title,
                                                     'invoice_no': invoice_no, 'is_exp': 'false', 'pk': pk,
                                                 'slug': slug})

            #     invoice_exists = r.hexists(name=company.id, key=invoice_no)
            #     if invoice_exists:
            #         key = r.hget(name=company.id, key=invoice_no)
            #         a = r.hgetall(name=key)
            #         for i, j in a.items():
            #             l = list(r.smembers(name=j))
            #             initials[int(i.decode('utf-8'))] = list(str(l[0].decode('utf-8').strip('][').split(', ')[0]).replace('"', '').split(','))
            #         print(initials)
            # return render(request, 'bill.html', {'bill_title': list_title, 'invoice_no': invoice_no, 'var': 0,
            #                                      'no_of_title': len(list_title), 'company': company, 'initials': initials})
    def post(self, request, pk, slug):
        Company.objects.filter(user=request.user, pk=pk, slug=slug).update(invoice_no=F('invoice_no')+1)
        return redirect(reverse_lazy('authentication:profile_url'))


def bill_pdf(request, pk, slug, bill_id):
    company = get_object_or_404(Company, user=request.user, pk=pk, slug=slug, active=True)
    bill_title = AddDefaultData.get_title(company=company)
    bill_data = get_object_or_404(FileStorage, pk=bill_id, user=request.user, company=company, active=True)
    result_data = json.loads(bill_data.result)
    data_dict = json.loads(bill_data.data)
    summation_field = []
    if r.exists('{}::summation_field'.format(pk)):
        summation_field = r.smembers('{}::summation_field'.format(pk))
        summation_field = [i.decode() for i in summation_field]
    j = 1
    final_data_dict = {}
    final_result_data = {}
    block = True
    for x, y in data_dict.items():
        temp_dict = {i: y[i] for i in bill_title}
        final_data_dict[j] = temp_dict
        j += 1
    print(final_data_dict)
    for x, y in result_data.items():
        if x in summation_field and y != '':
            if bill_data.gst:
                final_result_data[x] = float(y) + (float(y) * (float(bill_data.gst)*0.01))
                block = False
            if bill_data.cgst:
                final_result_data[x] = float(y) + (float(y) * (float(bill_data.cgst)*0.01))
                block = False
            if bill_data.igst:
                final_result_data[x] = float(y) + (float(y) * (float(bill_data.igst)*0.01))
                block = False
            if bill_data.sgst:
                block = False
                final_result_data[x] = float(y) + (float(y) * (float(company.sgst)*0.01))
            if block:
                break
    print(final_result_data)
    html = render_to_string('pdf/bill_pdf.html', {'company': company, 'dict': final_data_dict,
                                                  'title': bill_title, 'bill_data': bill_data,
                                                  'result_data': final_result_data})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="bill.pdf"'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT+
                                                                                 'css/pdf/bill_pdf.css')])
    return response

