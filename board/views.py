from django.shortcuts import render, redirect

# Create your views here.
#
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, ListView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from .models import BoardModel,ThreadModel
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# 検索機能
from django.db.models import Q

# ページング
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic

#from django.contrib.admin.widgets import AdminDateWidget
#ユーザの削除
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse


def homeview(request):
    return render(request, 'home.html')


def signupview(request):
    print(request.method)
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        try:
            user = User.objects.create_user(username_data, '', password_data)
            return redirect('login_original')
        except IntegrityError:
            return render(request, 'signup.html',
                          {'error': 'このユーザーは既に登録されています'})
    else:
        print(User.objects.all())
        return render(request, 'signup.html')
    return render(request, 'signup.html')


def guest(request):
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        user = authenticate(request,
                            username=username_data,
                            password=password_data)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('guest')
    return render(request, 'guest.html')


def loginview(request):
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        user = authenticate(request,
                            username=username_data,
                            password=password_data)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('login_original')
    return render(request, 'login_original.html')


def logoutview(request):
    logout(request)
    return redirect('home')

#"""
class BoardList(LoginRequiredMixin, generic.ListView):
    template_name = 'list.html'
    paginate_by = 10
    model = ThreadModel


    def get_queryset(self):
        q_word = self.request.GET.get('query')
        #ページング別の方法
        #print(q_word)
        #page = self.request.GET.get('page')
        """
        if q_word == "new":
            object_list = BoardModel.objects.order_by("postdate").filter(
                author=self.request.user)
        elif q_word == "new2":
            object_list = BoardModel.objects.order_by("deadline").filter(
                author=self.request.user)
        """
        if q_word:
            object_list = BoardModel.objects.filter(author=self.request.user | Q(title__icontains=q_word)| Q(category__icontains=q_word))
        else:
            object_list = ThreadModel.objects.all().order_by("-postdate")
            #object_list = BoardModel.objects.order_by("-postdate").filter(author=self.request.user)
            #paginator = Paginator(object_list, 2)
            #pages = paginator.get_page(page)
        return object_list



"""
@login_required
def ListView(request):
    object_list = BlogModel.objects.all()
    return render(request,'list.html',{'object_list':object_list})
"""


class BoardDetail(DetailView):
    template_name = 'detail.html'
    model = ThreadModel


class BoardCreate(CreateView):
    template_name = 'create.html'
    model = ThreadModel
    fields = ('title', 'content','author')
    success_url = reverse_lazy('list')


    def get_initial(self):
        initial = super().get_initial()
        initial["author"] = self.request.user
        return initial




class BoardList2(generic.ListView):
    model = BoardModel
    paginate_by = 20

    def get_queryset(self):
        code = self.kwargs['pk']
        object_list=BoardModel.objects.order_by("-postdate").filter(target=code)
        return object_list



class BoardCreate2(CreateView):
    template_name = 'list_view.html'
    model = BoardModel
    fields = ('human', 'content', 'target')
    paginate_by = 20
    #success_url = reverse_lazy('list1/)

    def get_initial(self, **kwargs):
        q_word = self.request.GET.get('query')
        initial = super().get_initial()
        initial["target"] = self.kwargs.get('pk')

        if q_word:
            q_word = ">>"+q_word
            initial["content"] = q_word
        return initial

    def get_success_url(self):
        return reverse('list_view', kwargs={'pk': self.kwargs['pk']})




class FormAndListView(BoardCreate2, BoardList2):

    def get(self, request, *args, **kwargs):
        formView = BoardCreate2.get(self, request, *args, **kwargs)
        listView = BoardList2.get(self, request, *args, **kwargs)
        formData = formView.context_data['form']
        listData = listView.context_data['object_list']
        page = listView.context_data['page_obj']
        context = {'form' : formData,'object_list' : listData,'page_obj':page}
        return render(request, 'list_view.html', context)


class BoardDelete(DeleteView):
    template_name = 'delete.html'
    model = ThreadModel
    success_url = reverse_lazy('list')


class BoardUpdate(UpdateView):
    template_name = 'update.html'
    model = ThreadModel
    fields = ('title', 'author','content',)
    success_url = reverse_lazy('list')

    def get_initial(self, **kwargs):
        initial = super().get_initial()
        initial["author"] = self.request.user
        return initial


class PasswordChange(PasswordChangeView):
    template_name = 'password_change_original.html'
    success_url = reverse_lazy('password_change_done_original')


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'password_change_done_original.html'


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.username == self.kwargs['username'] or user.is_superuser


class UserDeleteView(OnlyYouMixin, DeleteView):
    template_name = "userdelete.html"
    success_url = reverse_lazy("home")
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
