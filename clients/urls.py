#clients/urls.py
from django.urls import path,include

import buisness.views
from . import views
import buisness
from django.contrib.auth import views as auth_views

urlpatterns = [
     path("dashboard",views.clientindex,name='clientindex'),
     path("CompleteCompilance",views.CompleteCompilance,name='complete_compilance'),
     path('entity/<int:pk>/',views.entityandfilings,name='entity'),
     path("business/<int:pk>/",views.buisnesslocation,name='business'),
     path("phone/<int:pk>/",views.phones,name='phones'),
     path("website/<int:pk>/",views.websites,name='website'),   
     path("ein/<int:pk>/",views.ein,name='ein'),  
     path("banking/<int:pk>/",views.banking,name='banking'),
     path("agencies/<int:pk>/",views.agencies,name='agencies'),
     path("sos_contact/<int:pk>/", views.sos_contact_list, name="sos_contact_list"),
     path("register_business", buisness.views.register_business, name="business_registration"),
     path("signup", views.signup_view, name="signup"),
     path("login/", views.login_view, name="login"),
     path("reset_password/", views.reset_password, name="forget_pswrd"),
     path("logout", auth_views.LogoutView.as_view(), name="logout"),
     
     path('businessplan/<int:pk>/',views.businessplan,name='businessplan'),
     path("businessassets/<int:pk>/",views.business_assets,name='business_assets'),
     path("corponlyfacts/<int:pk>/",views.corponlyfacts,name='corponlyfacts'),
     path("bankrating/<int:pk>/",views.Bank_rating,name='bankrating'),
     path("businessloan/<int:pk>/",views.Cd_loan,name='businessloan'),
     path("comparablecredit/<int:pk>/",views.Comparable_credit,name='comparablecredit'),
]