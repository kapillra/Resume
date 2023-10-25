from django.urls import path
from .views import *

urlpatterns = [
    path('', login_page, name='login_page'),
    path('register_page/', register_page, name='register_page'),
    path('otp_page/', otp_page, name='otp_page'),
    path('forgot_password_page/', forgot_password_page, name='forgot_password_page'),
    path('recover_password_page/', recover_password_page, name='recover_password_page'),
    path('profile_page/', profile_page, name='profile_page'),

    # functionality urls
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('otp_verify/<str:verify_for>/', otp_verify, name='otp_verify'),

    path('update_profile/', update_profile, name="update_profile"),
    path('upload_image/', upload_image, name="upload_image"),

    # education
    path('add_education/', add_education, name="add_education"),
    path('edit_education_page/<int:pk>/', edit_education_page, name="edit_education_page"),
    path('edit_education/<int:pk>/', edit_education, name="edit_education"),
    path('delete_education/<int:pk>/', delete_education, name="delete_education"),
    
    # experience
    path('add_experience/', add_experience, name="add_experience"),
    path('edit_experience_page/<int:pk>/', edit_experience_page, name="edit_experience_page"),
    path('edit_experience/<int:pk>/', edit_experience, name="edit_experience"),
    path('delete_experience/<int:pk>/', delete_experience, name="delete_experience"),
    path('add_skills/', add_skills, name="add_skills"),
    path('delete_skill/<int:pk>/', delete_skill, name="delete_skill"),

    path('view_resume/@<str:user_id>/', view_resume, name="view_resume"),
    path('get_in_touch/@<str:user_id>/', get_in_touch, name="get_in_touch"),


    path('logout/', logout, name='logout'),

    # functionality url
]