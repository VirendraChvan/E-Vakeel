
from django.contrib import admin
from django.urls import path,include
from. import views
urlpatterns = [
    
    path('',views.index,name='index'),
    path('home',views.index,name='home'),
    path('send_msg',views.send_msg,name='send_msg'),
    path('sub_blog',views.sub_blog,name='sub_blog'),
    path('book_appointment',views.book_appointment,name='book_appointment'),
    path('blog_menu',views.blog_menu,name='blog_menu'),
    path('blog_temp/<id>/',views.blog_temp,name='blog_temp'),
    path('blog_comment/<id>/',views.blog_comment,name='blog_comment'),

    #admin urls
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_register',views.admin_register,name='admin_register'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('admin_msg',views.admin_msg,name='admin_msg'),
    path('admin_team',views.admin_team,name='admin_team'),
    path('admin_update',views.admin_update,name='admin_update'),
    path('logout_admin',views.logout_admin,name='logout_admine'),
    path("delete_msg",views.delete_msg,name='delete_msg'),
    path("add_team",views.add_team,name='add_team'),
    path("delete_team",views.delete_team,name='delete_team'),
    path("update_team/<id>/",views.update_team,name='update_team'),
    path("Appointment_section",views.Appointment_section,name='Appointment_section'),
    path("Create_appointment",views.Create_appointment,name='Create_appointment'),
    path("add_appointment",views.add_appointment,name='add_appointment'),
    path("update_appointment/<id>/",views.update_appointment,name='update_appointment'),
    path("delete_appointment",views.delete_appointment,name='delete_appointment'),
    path("blog_dash",views.blog_dash,name='blog_dash'),
    path("add_blog",views.add_blog,name='add_blog'),
    path("delete_blog",views.delete_blog,name='delete_blog'),
    path("update_blog/<id>/",views.update_blog,name='update_blog'),
    path("all_comment",views.all_comment,name='all_comment'),
    path("delete_comment",views.delete_comment,name='delete_comment'),
    path("all_subs",views.all_subs,name='all_subs'),
    path("delete_subs",views.delete_subs,name='delete_subs'),
    path("delete_noti",views.delete_noti,name='delete_noti'),
    path("delete_noti_all",views.delete_noti_all,name='delete_noti_all'),
    path("sub_admin",views.sub_admin,name='sub_admin'),
    path("sub_admin_delete",views.sub_admin_delete,name='sub_admin_delete'),
]
