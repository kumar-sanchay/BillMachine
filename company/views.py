import redis
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import CreateView, DetailView, View, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateCompanyForm, SearchFieldForm
from .models import BillTitle, Company
from authentication.models import UserModel
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from fileStorage.models import FileStorage
from essentials.tasks import change_search_field


r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class CreateCompany(LoginRequiredMixin, CreateView):
    template_name = 'company_form.html'
    form_class = CreateCompanyForm

    def form_valid(self, form):
        new_company = form.save(commit=False)
        self.company_detail = new_company
        new_company.user = self.request.user
        new_company.active = True
        new_company.save()
        data_dict = {}
        request_dict = self.request.POST.getlist('input')
        j = 1
        while True:
            try:
                if len(request_dict) == 0:
                    break
                key = 'title' + str(j)
                val = request_dict.pop(0)
                data_dict[key] = val

                if j == 5:
                    BillTitle.objects.create(company=new_company, **data_dict)
                    j = 0
                    data_dict.clear()
                j = j + 1
            except Exception as e:
                break
        if j % 5 != 0:
            BillTitle.objects.create(company=new_company, **data_dict)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('company:detail_company',kwargs={'slug': self.company_detail.slug,
                                                                 'pk':self.company_detail.pk})

    def get_context_data(self, **kwargs):
        context = super(CreateCompany, self).get_context_data(**kwargs)
        context['company'] = Company.objects.filter(user=self.request.user, active=True)
        return context


class CompanyDetail(LoginRequiredMixin, View):

    def get(self, request, pk, slug):
        comp = Company.objects.filter(user=request.user, active=True)
        c = get_object_or_404(Company, user=request.user, pk=pk, slug=slug, active=True)
        bills = FileStorage.objects.filter(user=request.user, company=c, active=True)
        paginator = Paginator(bills, 6)
        page = request.GET.get('page')
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            bills = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return render(request, 'bill_display.html', {'company': comp, 'c': c, 'bills': bills})
        return render(request, 'company_detail.html', {'company': comp, 'c': c, 'bills': bills})




