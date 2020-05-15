from django.shortcuts import render, redirect, HttpResponse
from .forms import LoginForm, RegisterForm, ChangePersonalDetailsForm
from django.views.generic import FormView, CreateView, DetailView, RedirectView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from .models import UserModel, RecentActivities
from django.urls import reverse_lazy
from company.models import Company
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        if user is not None:
            login(self.request, user)
            self.user = user
        else:
            return render(self.request, 'login.html', {'error':'Username or Password Incorrect.'})
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('authentication:profile_url')


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = 'authentication:profile_url'

    def form_valid(self, form):
        user = form
        new_user = user.save(commit=False)
        new_user.set_password(user.cleaned_data['password1'])
        new_user.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        company = Company.objects.filter(user=user, active=True)
        activity = RecentActivities.objects.filter(user=request.user, active=True).order_by('-created')
        paginator = Paginator(activity, 5)
        page = request.GET.get('page')

        try:
            activity = paginator.page(page)
        except PageNotAnInteger:
            activity = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            activity = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return render(request, 'activity.html', {'user': user, 'company': company, 'activity': activity})
        return render(request, 'profile.html', {'user': user, 'company': company, 'activity': activity})


class ProfileSettings(LoginRequiredMixin, TemplateView):
    template_name = 'settings/settings_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileSettings, self).get_context_data(**kwargs)
        context['company'] = Company.objects.filter(user=self.request.user, active=True)
        return context


class ChangePersonalDetails(LoginRequiredMixin, FormView):

    form_class = ChangePersonalDetailsForm
    template_name = 'settings/change_personal_details.html'

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        state = form.cleaned_data['state']
        city = form.cleaned_data['city']
        try:
            UserModel.objects.filter(pk=self.request.user.pk).update(first_name=first_name,
                                                                     last_name=last_name,
                                                                     city=city,
                                                                     state=state)
        except Exception as e:
            pass
        return super(ChangePersonalDetails, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChangePersonalDetails, self).get_context_data(**kwargs)
        context['company'] = Company.objects.filter(user=self.request.user, active=True)
        return context

    def get_initial(self):
        initial_val = super(ChangePersonalDetails, self).get_initial()
        initial_val['first_name'] = self.request.user.first_name
        initial_val['last_name'] = self.request.user.last_name
        initial_val['city'] = self.request.user.city
        initial_val['state'] = self.request.user.state
        return initial_val

    def get_success_url(self):
        return reverse_lazy('authentication:profile_settings')