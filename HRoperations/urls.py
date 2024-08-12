from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('generate_filled_pdf/<int:employee_id>/', views.generate_filled_pdf, name='generate_filled_pdf'),
    path('check_email/', views.check_email, name='check_email'),
    path('send_email/', views.send_email_view, name='send_email'),
    path('employees/', views.employee_list, name='employee_list'),
    path('update_employee/', views.update_employee, name='update_employee'),
    path('delete_employee/', views.delete_employee, name='delete_employee'),

]

