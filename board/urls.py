from django.urls import path

from .views import BoardList, BoardDetail, BoardCreate, BoardDelete, BoardUpdate, signupview, loginview, logoutview, homeview, guest, PasswordChange, PasswordChangeDone, UserDeleteView, FormAndListView


urlpatterns = [
    path('list/', BoardList.as_view(), name='list'),
    path('list1/<int:pk>/', FormAndListView.as_view(), name='list1'),
    #path('list/', ListView, name='list'),
    path('detail/<int:pk>/', BoardDetail.as_view(), name='detail'),
    path('create/', BoardCreate.as_view(), name='create'),
    path('delete/<int:pk>', BoardDelete.as_view(), name='delete'),
    #path('userdelete/<int:pk>', UserDelete.as_view(), name='userdelete'),
    path('update/<int:pk>', BoardUpdate.as_view(), name='update'),
    path('signup', signupview, name='signup'),
    path('login1/', loginview, name='login1'),
    path('logout1/', logoutview, name='logout1'),
    path('home/', homeview, name='home'),
    path('guest/', guest, name='guest'),
    path('password_change1/',PasswordChange.as_view(),name='password_change1'),
    path('password_change_done1/',PasswordChangeDone.as_view(),name='password_change_done1'),
    path('<str:username>/userdelete/', UserDeleteView.as_view(), name='userdelete'),
    #path('create2/', BlogCreate2.as_view(), name='create2'),
]