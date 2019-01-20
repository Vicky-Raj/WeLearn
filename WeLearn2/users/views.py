from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserForm
from django.views.generic import View,TemplateView

class RegisterView(View):
    template_name = 'users/register.html'
    def get(self, request):
        form = UserForm()
        return render(request,self.template_name,{'form':form})
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for "{username}"')
            return redirect('login')
        else:
            return render(request,self.template_name,{'form':form})

class LogoutWarn(TemplateView):
    template_name = 'users/logout_warn.html'