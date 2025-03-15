from django.urls import path,include
from . import views
urlpatterns = [
     path("",views.index,name='index'),
     path('members/',views.membersearch,name='members'),
     path('tables/',views.viewmembers,name='table'),
     path('edit/<int:user_id>/', views.editmembers, name='edit_members'),
     path('loginasuser/<int:user_id>/',views.loginasuser,name='login_as_user'),
     path('delete/<int:user_id>/', views.deletemember, name='delete_member')

]
