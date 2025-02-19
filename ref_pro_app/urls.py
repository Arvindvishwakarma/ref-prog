from django.urls import path
from ref_pro_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contact', views.contact, name="contact"),
    path('faq', views.faq, name="faq"),
    path('privacypolicy', views.privacypolicy, name="privacypolicy"),
    path('referralguidelines', views.referralguidelines, name="referralguidelines"),
    path('profile', views.profile, name="profile"),
    path('refer', views.refer, name="refer"),
    path('about', views.about, name="about"),
    
    
    path('adminportal', views.adminportal, name="adminportal"),
    path('add', views.add, name="add"),
    path('edit', views.edit, name="edit"),
    path('delete/<str:id>', views.delete, name="delete"),
    path('update/<str:id>', views.update, name="update"),


    path('dashboard', views.dashboard, name="dashboard"),
    path('add_dash', views.add_dash, name="add_dash"),   
    path('edit_dash', views.edit_dash, name="edit_dash"),        
    path('update_dash/<str:id>', views.update_dash, name="update_dash"),
    

    path('withdraw_admin', views.withdraw_admin, name="withdraw_admin"),
    path('withdraw_add', views.withdraw_add, name="withdraw_add"),
    path('withdraw_edit', views.withdraw_edit, name="withdraw_edit"),
    path('withdraw_delete/<str:id>', views.withdraw_delete, name="withdraw_delete"),
    path('withdraw_update/<str:id>', views.withdraw_update, name="withdraw_update"),


    path('dash_withdraw', views.dash_withdraw, name="dash_withdraw"),
    path('add_withdraw', views.add_withdraw, name="add_withdraw"),
    path('edit_withdraw', views.edit_withdraw, name="edit_withdraw"),
    path('update_withdraw/<str:id>', views.update_withdraw, name="update_withdraw"),

]