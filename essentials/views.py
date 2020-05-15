import redis
import re
import pickle
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from company.models import Company, BillTitle
from django.http import HttpResponse
from django.contrib.auth.views import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from company.forms import CreateCompanyForm
from .tasks import change_field, change_search_field
from django.forms import model_to_dict


r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Settings(LoginRequiredMixin, TemplateView):
    template_name = 'settings/company_settings_lists.html'

    def get_context_data(self, **kwargs):
        context = super(Settings, self).get_context_data(**kwargs)
        context['company'] = Company.objects.filter(user=self.request.user, active=True)
        context['company_pk'] = self.kwargs['pk']
        context['company_slug'] = self.kwargs['slug']
        return context


class AddDefaultData(LoginRequiredMixin, View):
    @classmethod
    def get_title(cls, company) -> list:
        titles = []
        bill_title = BillTitle.objects.filter(company=company, active=True)
        for bill in bill_title.iterator():
            if bill.title1:
                titles.append(bill.title1)
            if bill.title2:
                titles.append(bill.title2)
            if bill.title3:
                titles.append(bill.title3)
            if bill.title4:
                titles.append(bill.title4)
            if bill.title5:
                titles.append(bill.title5)
        return titles

    def get(self, request, slug, pk):
        single_company = get_object_or_404(Company, slug=slug, pk=pk)
        company = Company.objects.filter(user=request.user, active=True)
        if single_company.user == self.request.user:
            title = AddDefaultData.get_title(single_company)
            name = 'company::search_fields'
            key = '{}::{}'.format(slug, pk)
            if r.hexists(name, key):
                required = r.hget(name, key)
                return render(self.request, 'settings/add_default_data.html', {'title': title, 'required':
                    required.decode(), 'company': company})
            else:
                return redirect(Company.get_search_url(single_company))
        return HttpResponse('Unauthenticated.')

    def post(self, request, slug, pk):
        detail_dict = request.POST
        last_index = 1
        name = 'company::search_fields'
        key = '{}::{}'.format(slug, pk)
        attr = r.hget(name, key)
        if r.hexists(name='{}::{}'.format(pk, 'search_fields'), key='last_index'):
            r.hincrby(name='{}::{}'.format(pk, 'search_fields'), key='last_index', amount=1)
            last_index = r.hget(name='{}::{}'.format(pk, 'search_fields'), key='last_index')
            last_index = last_index.decode()
        else:
            r.hset(name='{}::{}'.format(pk, 'search_fields'), key='last_index', value=last_index)
        for k, val in detail_dict.items():
            if k != "csrfmiddlewaretoken":
                r.hset("{}::{}".format(pk, last_index), key=k, value=val)
        r.hset(name='{}::{}'.format(pk, 'search_fields'), key=detail_dict[attr.decode()], value=last_index)
        return redirect(reverse_lazy('essentials:company_settings', args=[pk, slug]))


class AddExpressionsToFields(LoginRequiredMixin, View):

    def get(self, request, pk, slug):
        single_company = get_object_or_404(Company, pk=pk, slug=slug, user=self.request.user)
        title = AddDefaultData.get_title(company=single_company)
        company = Company.objects.filter(user=request.user, active=True)
        title_dict = {key: '' for key in title}
        if r.hexists('company::expressions', '{}::{}'.format(slug, pk)):
            exp_dict = r.hget('company::expressions', '{}::{}'.format(slug, pk))
            try:
                exp_dict = pickle.loads(exp_dict)
                for k, v in title_dict.items():
                    if k in exp_dict:
                        title_dict[k] = exp_dict[k]
            except (pickle.UnpicklingError, pickle.PickleError, pickle.PickleError, Exception) as e:
                pass
        print(title_dict)
        return render(request, 'settings/add_expressions.html', {'title': title_dict, 'company': company})

    def post(self, request, pk, slug):
        detail_dict = {}
        for x, y in request.POST.items():
            if not x == 'csrfmiddlewaretoken':
                detail_dict[x] = y
        try:
            for x, y in detail_dict.items():
                e_lst = r'[A-Z][\w]*[$a-z0-9]'
                print(re.findall(e_lst, y))
            enocoded_dict = pickle.dumps(detail_dict)
            print(detail_dict)
            name = 'company::expressions'
            key = '{}::{}'.format(slug, pk)
            if r.hexists(name, key):
                r.hdel(name, key)
            r.hset(name, key, enocoded_dict)
            return redirect(reverse_lazy('essentials:company_settings', args=[pk, slug]))
        except (pickle.UnpicklingError, pickle.PicklingError) as e:
            return HttpResponse(e)
        except Exception as e:
            return HttpResponse(e)


class AddTotalField(LoginRequiredMixin, View):

    def get(self, request, pk, slug):
        company = get_object_or_404(Company, pk=pk, slug=slug, user=self.request.user)
        title = AddDefaultData.get_title(company)
        name = "{}::{}".format("total_fields", pk)
        lst = []
        if r.exists(name):
            result = r.smembers(name)
            lst = [i.decode() for i in result]
        return render(request, 'add_total_field.html', {'title': title, 'lst': lst, 'pk': pk, 'slug': slug})

    def post(self, request, pk, slug):
        total = request.POST.getlist('total_field')
        name = "{}::{}".format("total_fields", pk)
        for i in total:
            r.sadd(name, i)
        return redirect(reverse_lazy("essentials:settings", args=[pk, slug]))


class CompanyDetailsSetting(LoginRequiredMixin, FormView):
    form_class = CreateCompanyForm
    template_name = 'settings/company_details_settings.html'

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        print(cleaned_data)
        c = get_object_or_404(Company, user=self.request, pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        c.update(cleaned_data)
        return super(CompanyDetailsSetting, self).form_valid(form)

    def form_invalid(self, form):
        print('Invalid')
        return HttpResponse('Invalid')

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailsSetting, self).get_context_data(**kwargs)
        context['company'] = Company.objects.filter(user=self.request.user, active=True)
        return context

    def get_form_kwargs(self):
        kwargs = super(CompanyDetailsSetting, self).get_form_kwargs()
        c = get_object_or_404(Company, user=self.request.user, pk=self.kwargs['pk'],
                              slug=self.kwargs['slug'])
        data_dict = model_to_dict(instance=c, exclude=['user', 'id', 'slug', 'signature', 'created', 'active'])
        kwargs['data'] = data_dict
        return kwargs

    def get_success_url(self):
        return reverse_lazy('essentials:company_settings', args=[self.kwargs['pk'], self.kwargs['slug']])


class AddorDeleteFields(LoginRequiredMixin, View):
    def get(self, request, pk, slug):
        company = Company.objects.filter(user=request.user, active=True)
        c = get_object_or_404(Company, pk=pk, slug=slug, active=True)
        bill_title = AddDefaultData.get_title(company=c)
        name = 'company::search_fields'
        key = '{}::{}'.format(slug, pk)
        search_field = b''
        if r.hexists(name, key):
            search_field = r.hget(name, key)
        return render(request, 'settings/add_or_delete_field_settings.html', {'company': company,
                                                                               'bill_title': bill_title,
                                                                              'search_field': search_field.decode()})

    def post(self, request, pk, slug):
        company = get_object_or_404(Company, user=request.user, pk=pk, slug=slug)
        request_dict = request.POST.getlist('input')
        print(request.POST.getlist('input'))
        bill = BillTitle.objects.filter(company=company, active=True)
        for bill_title in bill:
            bill_title.delete()
        data_dict = {}
        j = 1
        while True:
            try:
                if len(request_dict) == 0:
                    break
                key = 'title'+str(j)
                val = request_dict.pop(0)
                data_dict[key] = val

                if j == 5:
                    BillTitle.objects.create(company=company, **data_dict)
                    j = 0
                    data_dict.clear()
                j = j + 1
            except Exception as e:
                break
        if j % 5 !=0 :
            BillTitle.objects.create(company=company, **data_dict)
        change_field.delay(pk, slug, request.POST.getlist('input'))

        return redirect(reverse_lazy('essentials:company_settings', args=[pk, slug]))


class CompanySearchField(LoginRequiredMixin, View):

    def get(self, request, pk, slug, *args, **kwargs):
        lst = []
        name = 'company::search_fields'
        key = '{}::{}'.format(slug, pk)
        search_field = 'None'
        single_company = get_object_or_404(Company, user=self.request.user, pk=pk, slug=slug)
        bill_title = BillTitle.objects.filter(company=single_company)
        company = Company.objects.filter(user=request.user, active=True)
        for bill in bill_title.iterator():
            if bill.title1:
                lst.append(bill.title1)
            if bill.title2:
                lst.append(bill.title2)
            if bill.title3:
                lst.append(bill.title3)
            if bill.title4:
                lst.append(bill.title4)
            if bill.title5:
                lst.append(bill.title5)
        lst.append('None')
        if r.hexists(name, key):
            search_field = r.hget(name, key)
            search_field = search_field.decode()
        return render(request, 'settings/company_search_field.html', {'list': lst, 'user': self.request.user,
                                                                      'search_field': search_field, 'company': company})

    def post(self, request, slug, pk):
        radio = self.request.POST.get('n')
        name = 'company::search_fields'
        key = '{}::{}'.format(slug, pk)
        # if r.hexists(name=name, key=key):
        #     r.hdel(name, key)
        # r.hset(name, key, radio)
        print(radio)
        change_search_field.delay(radio, pk, slug)
        return redirect(reverse_lazy('essentials:company_settings', args=[pk, slug]))


class ShowDefaultData(LoginRequiredMixin, View):

    def get(self, request, pk, slug):
        company = Company.objects.filter(user=request.user, active=True)
        cursor = request.GET.get('cur', 1)
        data_list = {}
        data_dict = {}
        i = 0
        if r.hexists(name="{}::{}".format(pk, 'search_fields'), key='last_index'):
            while i != 20:
                if cursor != 'NaN':
                    if r.exists('{}::{}'.format(pk, cursor)):
                        data_dict = r.hgetall(name='{}::{}'.format(pk, cursor))
                        data_dict = {k.decode(): y.decode() for k, y in data_dict.items()}
                        data_list[cursor] = data_dict
                    i = i + 1
                    print(cursor)
                    print(type(cursor))
                    cursor = eval('{}+{}'.format(cursor, 1))
                else:
                    break
            print(data_list)
        if request.is_ajax():
            print('yup')
            return render(request, 'settings/default_data_table.html', {'company': company, 'data_list': data_list,
                                                                      'cursor': cursor, 'heading': data_dict.keys()})
        return render(request, 'settings/show_default_data.html', {'company': company, 'data_list': data_list,
                                                                  'cursor': cursor, 'heading': data_dict.keys(),
                                                                   'pk': pk, 'slug': slug})


class DeleteDefaultData(LoginRequiredMixin, View):

    def post(self, request, pk, slug):
        try:
            index = request.POST.get('index')
            if r.exists("{}::{}".format(pk, index)) \
                    and r.hexists(name='company::search_fields', key='{}::{}'.format(slug, pk)):
                search_field = r.hget(name='company::search_fields', key='{}::{}'.format(slug, pk))
                search_field = search_field.decode()
                r.delete("{}::{}".format(pk, index))
                r.hdel('{}::{}'.format(pk, 'search_fields'),search_field)
                return JsonResponse({'status': 'ok'})
            return JsonResponse({'status': 'failure'})
        except Exception as e:
            return JsonResponse({'status': 'failure'})


class AddSummationField(LoginRequiredMixin, View):

    def get(self, request, pk, slug):
        company = Company.objects.filter(user=request.user, active=True)
        c = company.get(pk=pk, slug=slug)
        title = AddDefaultData.get_title(c)
        summation_fields = []
        if r.exists('{}::summation_field'.format(pk)):
            summation_fields = r.smembers('{}::summation_field'.format(pk))
            summation_fields = [i.decode() for i in summation_fields]
        return render(request, 'settings/add_summation_field.html', {'list': title, 'summation_field': summation_fields})

    def post(self, request, pk, slug):
        summation_field = request.POST.getlist('n')
        if r.exists('{}::summation_field'.format(pk)):
            r.delete('{}::summation_field'.format(pk))
        for i in summation_field:
            r.sadd('{}::summation_field'.format(pk), i)
        print(summation_field)
        return redirect(reverse_lazy('essentials:company_settings', args=[pk, slug]))