from django.urls import path

from .views import BoardList, BoardDetail, BoardCreate, BoardDelete, BoardUpdate, signupview, loginview, logoutview, homeview, guest, PasswordChange, PasswordChangeDone, UserDeleteView, FormAndListView, evaluationview


urlpatterns = [
    path('list/', BoardList.as_view(), name='list'),
    path('list_view/<int:pk>/', FormAndListView.as_view(), name='list_view'),
    #path('list/', ListView, name='list'),
    path('detail/<int:pk>/', BoardDetail.as_view(), name='detail'),
    path('create/', BoardCreate.as_view(), name='create'),
    path('delete/<int:pk>', BoardDelete.as_view(), name='delete'),
    #path('userdelete/<int:pk>', UserDelete.as_view(), name='userdelete'),
    path('update/<int:pk>', BoardUpdate.as_view(), name='update'),
    path('signup', signupview, name='signup'),
    path('login_original/', loginview, name='login_original'),
    path('logout_original/', logoutview, name='logout_original'),
    path('home/', homeview, name='home'),
    path('guest/', guest, name='guest'),
    path('password_change_original/',PasswordChange.as_view(),name='password_change_original'),
    path('password_change_done_original/',PasswordChangeDone.as_view(),name='password_change_done_original'),
    path('<str:username>/userdelete/', UserDeleteView.as_view(), name='userdelete'),
    path('evaluation/<int:pk>/<int:pk2>', evaluationview, name='evaluation'),
]