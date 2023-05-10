from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from accounts.forms import SignUpForm, ConfForm
from accounts.models import Profile


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'


def confirmed_account(request):
    form = ConfForm()
    context = {'form': form}
    if request.method == 'POST':
        form = ConfForm(request.POST)
        if form.is_valid():
            user = request.user
            code = form.cleaned_data['code']
            if Profile.objects.filter(user=user, code=code):
                profile = Profile.objects.get(user=user)
                profile.is_confirmed = True
                profile.save()

                return redirect('/board')
            else:
                form = ConfForm()
                context = {'form': form, 'message': 'Неправильный код'}
    return render(request, 'registration/verify.html', context)



