from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View,ListView,DeleteView,TemplateView
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Pack,Tag,Link,Notification
from .forms import PackCreateForm,LinkCreateForm,UserEditForm,ProfileEditForm
from django.contrib.auth.models import User

class HomeView(ListView):
    template_name = 'home/index.html'
    cache_timeout = 1
    context_object_name = 'packs'
    def get_queryset(self):
        return Pack.objects.all()

class PackCreateView(LoginRequiredMixin,View):
    template_name = 'home/pack_create.html'
    def get(self,request):
        form = PackCreateForm()
        return render(request,self.template_name,context={'form':form})

    def post(self,request):
        form = PackCreateForm(request.POST)
        if form.is_valid():
            pack = Pack(author=request.user,
            title=form.cleaned_data.get('title'),
            description=form.cleaned_data.get('description')
            )
            pack.save()
            for tag in form.cleaned_data.get('tags').split(','):
                temp_tag,c = Tag.objects.get_or_create(tag=tag)
                temp_tag.pack.add(pack)
                temp_tag.save()
            for follower in request.user.profile.followers.all():
                notification = Notification(new_pack=True,from_user=request.user,to_user=follower,pack=pack)
                notification.save()
            return redirect('detail-view',pk=pack.pk)
        return render(request,self.template_name,{'form':form})


class LinkCreateView(LoginRequiredMixin,UserPassesTestMixin,View):
    template_name = 'home/link_create.html'

    def test_func(self):
        pack = get_object_or_404(Pack,pk=self.kwargs['pk'])
        return pack.author == self.request.user
    
    def get(self, request, pk):
        form = LinkCreateForm()
        return render(request,self.template_name,{'form':form,'pk':pk})

    def post(self, request,pk):
        pack = get_object_or_404(Pack, pk=pk)
        form = LinkCreateForm(request.POST)
        if form.is_valid():
            link = Link(
            title = form.cleaned_data.get('title'),
            description = form.cleaned_data.get('description'),
            link = form.cleaned_data.get('link'),
            link_color = form.cleaned_data.get('link_color'),
            text_color = form.cleaned_data.get('text_color'),
            pack = pack
            )
            link.save()
            for follower in request.user.profile.followers.all():
                notification = Notification(link_add=True,from_user=request.user,to_user=follower,pack=pack)
                notification.save()
            return redirect('detail-view',pk=pack.pk)
        return render(request,self.template_name,{'form':form,'pk':pk})

class PackDetailView(View):
    template_name = 'home/pack_detail.html'
    def get(self, request, pk):
        pack = get_object_or_404(Pack, pk=pk)
        return render(request,self.template_name,{'pack':pack,'comments':pack.comment_set.all().order_by('-date')})

class PackEditView(LoginRequiredMixin,UserPassesTestMixin,View):
    template_name = 'home/pack_create.html'

    def test_func(self):
        pack = get_object_or_404(Pack,pk=self.kwargs['pk'])
        return pack.author == self.request.user


    def get(self, request, pk):
        pack = get_object_or_404(Pack, pk=pk)
        form = PackCreateForm(initial={
            'title': pack.title,
            'description': pack.description,
            'tags': ','.join([tag.tag for tag in pack.tag_set.all()])
            })
        return render(request,self.template_name,{'form':form,'edit':True,'pk':pack.pk})

    def post(self, request, pk):
        pack = get_object_or_404(Pack, pk=pk)
        form = PackCreateForm(request.POST)
        if form.is_valid():
            pack.tag_set.clear()
            pack.title = form.cleaned_data.get('title')
            pack.description = form.cleaned_data.get('description')
            pack.save()
            for tag in form.cleaned_data.get('tags').split(','):
                temp_tag,c = Tag.objects.get_or_create(tag=tag)
                temp_tag.pack.add(pack)
                temp_tag.save()
            return redirect('detail-view',pk=pack.pk)
        return(request,self.template_name,{'form':form,'edit':True,'pk':pack.pk})

class LinkEditView(LoginRequiredMixin,UserPassesTestMixin,View):
    template_name = 'home/link_create.html'

    def test_func(self):
        link = get_object_or_404(Link, pk=self.kwargs['pk'])
        return link.pack.author == self.request.user

    def get(self, request, pk):
        link = get_object_or_404(Link, pk=pk)
        form = LinkCreateForm(initial={
            'title':link.title,
            'description':link.description,
            'link':link.link,
            'text_color':link.text_color,
            'link_color':link.link_color
        })
        return render(request, self.template_name, {'form':form,'edit':True,'pk':link.pack.pk})
    
    def post(self, request, pk):
        link = get_object_or_404(Link, pk=pk)
        form = LinkCreateForm(request.POST)
        if form.is_valid():
            link.title = form.cleaned_data.get('title')
            link.description = form.cleaned_data.get('description')
            link.link = form.cleaned_data.get('link')
            link.link_color = form.cleaned_data.get('link_color')
            link.text_color = form.cleaned_data.get('text_color')
            link.save()
            return redirect('detail-view',pk=link.pack.pk)
        return render(request, self.template_name, {'form':form, 'edit':True,'pk':link.pack.pk})

class PackDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):

    def test_func(self):
        pack = get_object_or_404(Pack,pk=self.kwargs['pk'])
        return self.request.user == pack.author

    model = Pack
    template_name = 'home/pack_delete.html'
    context_object_name = 'pack'
    success_url = reverse_lazy('home')

class LinkDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):

    template_name = 'home/link_delete.html'

    def test_func(self):
        link = get_object_or_404(Link, pk=self.kwargs['pk'])
        return self.request.user == link.pack.author

    def get(self, request, pk):
        link = get_object_or_404(Link, pk=pk)
        return render(request, self.template_name, {'link':link,'pk':link.pack.pk})

    def post(self, request, pk):
        link = get_object_or_404(Link,pk=self.kwargs['pk'])
        pack = link.pack.pk
        link.delete()
        return redirect('detail-view',pk=pack)

class ProfileView(View):
    template_name = 'home/profile.html'

    def get(self, request, pk):
        re_user = get_object_or_404(User,pk=pk)
        tab = request.GET.get('tab')
        if tab == 'pack':
            return render(request,
            self.template_name,
            {'re_user':re_user,
            'packs':re_user.pack_set.all(),
            'pack_view':True})

        elif tab == 'followers':
            return render(request,
            self.template_name,
            {'re_user':re_user,
            'followers':re_user.profile.followers.all(),
            'followers_view':True})
        
        elif tab == 'following' and re_user == request.user:
            return render(
                request,
                self.template_name,
                {'re_user':re_user,
                'following':request.user.follower_set.all(),
                'following_view':True})
        
        elif tab == 'liked':
            return render(
            request,
            self.template_name,
            {'re_user':re_user,
            'packs':re_user.likes_set.all(),
            'like_view':True})
    
        else:
            return render(request,
            self.template_name,
            {'re_user':re_user,
            'packs':re_user.pack_set.all(),
            'pack_view':True})

class ProfileEditView(LoginRequiredMixin, View):
    template_name = 'home/profile_edit.html'

    def get(self, request):
        us_form = UserEditForm(instance=request.user)
        pro_form = ProfileEditForm(instance=request.user.profile)
        return render(request,self.template_name,{'us_form':us_form,'pro_form':pro_form})

    def post(self, request):
        us_form = UserEditForm(request.POST, instance=request.user)
        pro_form = ProfileEditForm(request.POST,request.FILES,instance=request.user.profile)
        if us_form.is_valid() and pro_form.is_valid():
            us_form.save()
            pro_form.save()
            return HttpResponseRedirect('/user/'+str(request.user.pk)+'/profile?tab=packs')
        return render(request,self.template_name,{'us_form':us_form,'pro_form':pro_form})


class CategoryView(View):
    template_name = 'home/category.html'
    
    def get(self,request):
        if request.GET.get('tag') == None:
            return HttpResponseRedirect('/packs/category/?tag')
        tag = Tag.objects.filter(tag__istartswith=request.GET.get('tag')).first()
        if tag is None:
            return render(request,self.template_name,{'packs':None})    
        return render(request,self.template_name,{'packs':tag.pack.all()})

class NotificationView(LoginRequiredMixin, ListView):
    template_name = 'home/notification.html'
    context_object_name = 'notifs'
    def get_queryset(self):
        return self.request.user.to_user_set.all().order_by('-date')

class FavouriteView(LoginRequiredMixin, ListView):
    template_name = 'home/favourite.html'
    context_object_name = 'packs'
    def get_queryset(self):
        return self.request.user.likes_set.all()

class BookmarkView(LoginRequiredMixin, ListView):
    template_name = 'home/bookmark.html'
    context_object_name = 'packs'
    def get_queryset(self):
        return self.request.user.profile.bookmarks.all()

class SearchView(View):
    template_name = 'home/search.html'

    def get(self, request):
        packs = Pack.objects.annotate(search=SearchVector('title','description')).filter(search=request.GET.get('q'))
        return render(request,self.template_name,{'packs':packs})
        