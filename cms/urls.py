from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    
    # Jobs
    path('jobs/', views.jobs_list, name='jobs_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('apply-job/', views.apply_job, name='apply_job'),
    
    # Content pages
    path('about/', views.about_detail, name='about_detail'),
    path('services/', views.services_detail, name='services_detail'),
    path('contact/', views.contact_detail, name='contact_detail'),
    
    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    
    # Forms and AJAX
    path('contact-inquiry/', views.contact_inquiry, name='contact_inquiry'),
    path('ajax/jobs/', views.get_jobs_ajax, name='get_jobs_ajax'),
    path('ajax/office/<str:office_key>/', views.get_office_details, name='get_office_details'),
]
