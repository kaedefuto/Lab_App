from django.shortcuts import render, redirect

# Create your views here.
#
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, ListView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from .models import BoardModel
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


def homeview(request):
    return render(request, 'home.html')


def signupview(request):
    print(request.method)
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        try:
            user = User.objects.create_user(username_data, '', password_data)
            return redirect('login1')
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
            return redirect('login1')
    return render(request, 'login1.html')


def logoutview(request):
    logout(request)
    return redirect('home')


#"""
class BoardList(LoginRequiredMixin, generic.ListView):
    template_name = 'list.html'
    paginate_by = 10
    model = BoardModel


    def get_queryset(self):
        q_word = self.request.GET.get('query')
        #ページング別の方法
        #print(q_word)
        #page = self.request.GET.get('page')

        if q_word == "new":
            object_list = BoardModel.objects.order_by("postdate").filter(
                author=self.request.user)
        elif q_word == "new2":
            object_list = BoardModel.objects.order_by("deadline").filter(
                author=self.request.user)
        elif q_word:
            object_list = BoardModel.objects.filter(
                author=self.request.user | Q(title__icontains=q_word)
                | Q(category__icontains=q_word))
        else:
            #object_list2 = Folder.objects.all()
            #object_list = BlogModel.objects.all()
            object_list = BoardModel.objects.order_by("-postdate").filter(
                author=self.request.user)
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
    model = BoardModel


class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title', 'content', 'deadline', 'category', 'status', 'author')
    success_url = reverse_lazy('list')

    """
    def get_initial(self):
        initial = super().get_initial()
        initial["author"] = self.request.user
        return initial

    #widgets = {'deadline': AdminDateWidget()}
    """


class BoardList2(generic.ListView):
    paginate_by = 10
    model = BoardModel


class BoardCreate2(CreateView):
    template_name = 'list1.html'
    model = BoardModel
    fields = ('title', 'content', 'deadline', 'category', 'status', 'author')
    success_url = reverse_lazy('list1')


class FormAndListView(BoardCreate2,BoardList2):

    def get(self, request, *args, **kwargs):
        formView = BoardCreate.get(self, request, *args, **kwargs)
        listView = BoardList.get(self, request, *args, **kwargs)
        formData = formView.context_data['form']
        listData = listView.context_data['object_list']
        context = {'form' : formData,'object_list' : listData}
        return render(request, 'list1.html', context)


class BoardDelete(DeleteView):
    template_name = 'delete.html'
    model = BoardModel
    success_url = reverse_lazy('list')


"""
class UserDelete(DeleteView):
    template_name = 'userdelete.html'
    model = User
    success_url = reverse_lazy('home')
"""


class BoardUpdate(UpdateView):
    template_name = 'update.html'
    model = BoardModel
    fields = ('title', 'content', 'deadline', 'category', 'status')
    success_url = reverse_lazy('list')


"""
class BlogCreate2(CreateView):
    template_name = 'create2.html'
    model = Folder
    fields = ('title',)
    success_url = reverse_lazy('list')
"""


class PasswordChange(PasswordChangeView):
    template_name = 'password_change1.html'
    success_url = reverse_lazy('password_change_done1')


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'password_change_done1.html'


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
