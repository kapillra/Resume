from django.shortcuts import render, redirect
from .models import *
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from random import randint

# html page path
login_page_url = "resume_html_pages/login_page.html"
register_page_url = "resume_html_pages/register_page.html"
forgot_password_page_url = "resume_html_pages/forgot_password_page.html"
recover_password_page_url = "resume_html_pages/recover_password_page.html"
profile_page_url = "resume_html_pages/profile_page.html"
otp_page_url = "resume_html_pages/otp_page.html"
view_resume_url = "resume_view_page/index.html"

default_data = {
    'app_name': 'Resume Builder',
    'version': 1.0,
    'page_name_classes': ['login-page', 'register-page', 'sidebar-mini'],
}

# view resume
def view_resume(request, user_id):
    master = Master.objects.get(Email=f"{user_id}@gmail.com")
    user_profile = UserProfile.objects.get(Master=master)

    user_data = {
        'user_profile': user_profile,
        'skills': Skill.objects.filter(UserProfile=user_profile),
        'education': Education.objects.filter(UserProfile=user_profile),
        'experience': Experience.objects.filter(UserProfile=user_profile),
    }

    return render(request, view_resume_url, {'user_data':user_data})

# get in touch mail
def get_in_touch(request, user_id):
    send_from = request.POST['email']
    user_data = UserProfile.objects.get(UserID = user_id)
    send_to = [user_data.Master.Email,]

    # print(request.POST, send_from, send_to)
    send_mail(request.POST['subject'], request.POST['message'], send_from, send_to)

    return redirect(view_resume, user_id)

# send otp to mail
def send_otp(request, otp_for='reg'):
    send_to = [request.session['reg_data']['email'],]
    send_from = settings.EMAIL_HOST_USER

    otp = randint(1000, 9999)
    request.session['otp_data'] = {'otp': otp, 'otp_for': otp_for}
    # otp_data = {'otp': otp, 'otp_for': otp_for}
    print(otp)
    if otp_for == 'rec':
        subject = f'OTP for Recover Password'
        message = f"OTP for Recover Password is {otp}."
    else:
        subject = f'OTP for Registration'
        message = f"OTP for Registration is {otp}."

    send_mail(subject, message, send_from, send_to)

# otp verification
def otp_verify(request, verify_for='reg'):
    if request.session['otp_data']['otp'] == int(request.POST['otp']):
        if verify_for == 'rec':
            if request.POST['password'] == request.POST['confirm_password']:
                master = Master.objects.get(Email=request.session['reg_data']['email'])
                master.Password = request.POST['password']
                master.save()
                print('password changed successfully.')
                print('verify for', verify_for)
            else:
                print('both password must be same.')
                return redirect(recover_password_page)
            
        else:
            master = Master.objects.create(
                Email = request.session['reg_data']['email'],
                Password = request.session['reg_data']['password'],
                IsActive = True
            )
            UserProfile.objects.create(Master=master)
        
        return redirect(login_page)
    else:
        print('otp not matched')
    
    return redirect(otp_page)

# function to load profile data
def profile_data(request):
    master = Master.objects.get(Email=request.session['email'])
    
    user = UserProfile.objects.get(Master = master)
    
    split_name = user.FullName.split()
    user.first_name = split_name[0]
    user.last_name = split_name[-1]

    if len(split_name) == 3:
        user.middle_name = split_name[1]
    
    education = Education.objects.filter(UserProfile=user)[::-1]
    sr = 1
    for edu in education:
        edu.sr = sr
        sr += 1
    
    experience = Experience.objects.filter(UserProfile=user)[::-1]
    sr = 1
    for exp in experience:
        exp.sr = sr
        sr += 1

    default_data['user_data'] = user
    gender_option = {}


    default_data['education'] = education
    default_data['experience'] = experience
    default_data['skills'] = Skill.objects.filter(UserProfile=user)

    default_data['all_job_titles'] = sorted([job.JobTitle for job in Experience.objects.all()])

    sk_level = {}
    for sn, sl in skill_level:
        sk_level.setdefault(sn, sl)
    # print(sk_level)
    default_data['skill_level'] = sk_level


# login page view
def login_page(request):
    if 'email' in request.session:
        return redirect(profile_page)
    default_data['current_page_class'] = 'login-page'
    return render(request, login_page_url, default_data)

# register page view
def register_page(request):
    if 'email' in request.session:
        return redirect(profile_page)
    default_data['current_page_class'] = 'register-page'
    return render(request, register_page_url, default_data)

# forgot password page view
def forgot_password_page(request):
    if 'email' in request.session:
        return redirect(profile_page)
    default_data['current_page_class'] = 'login-page'
    return render(request, forgot_password_page_url, default_data)

# recover password page view
def recover_password_page(request):
    if 'email' in request.session:
        return redirect(profile_page)
    default_data['current_page_class'] = 'login-page'
    return render(request, recover_password_page_url, default_data)

# recover password page view
def otp_page(request):
    default_data['current_page_class'] = 'login-page'
    return render(request, otp_page_url, default_data)

# profile page view
def profile_page(request):
    if 'email' in request.session:
        default_data['current_page_class'] = 'sidebar-mini'
        default_data['current_page'] = 'profile_page'
        print('profile page called')

        profile_data(request) # calling profile_data function to load data
        
        return render(request, profile_page_url, default_data)
    return redirect(login_page)

# login functionality
def login(request):
    try:
        master = Master.objects.get(Email = request.POST['email'])
        if master.IsActive == False:
            if master.Password == request.POST['password']:
                # user = UserProfile.objects.get(Master=master)
                # default_data['user_data'] = user
                print('login success')
                request.session['email'] = master.Email
                
                return redirect(profile_page)
            else:
                print('incorrect password')
        else:
            print('this account is inactive.')
    except Master.DoesNotExist as err:
        print(err)

    return redirect(login_page)

# register functionality
def register(request):
    
    try:
        request.session['reg_data'] = {
            'email': request.POST['email'],
            'password': request.POST['password']
        }
        send_otp(request)
        return redirect(otp_page)
        
        
    except Exception as err:
        print(err)

    return redirect(register_page)

# forgot password functionality
def forgot_password(request):
    try:
        master = Master.objects.get(Email = request.POST['email'])

        request.session['forgot_pwd_data'] = {
            'email': master.Email,
            'for': 'rec'
        }

        send_otp(request, otp_for='rec')
        print('otp sent successfully.')
        return redirect(recover_password_page)
    except Master.DoesNotExist as err:
        print(err)

    return redirect(forgot_password_page)
from datetime import datetime

# profile update functionality
def update_profile(request):
    master = Master.objects.get(Email = request.session['email'])
    user = UserProfile.objects.get(Master=master)

    print(request.POST)

    full_name = [
        request.POST['first_name'],
        request.POST['middle_name'],
        request.POST['last_name']
    ]
    user.FullName = ' '.join(full_name)

    user.Gender = request.POST['gender']
    
    b_date = request.POST['birth_date']
    
    # b_date = '-'.join(b_date)
    # print(b_date)
    if b_date:
        b_date = b_date.split('/')[::-1]

        print(b_date, len(b_date))
        b_date = datetime(int(b_date[0]), int(b_date[2]), int(b_date[1]))

        user.BirthDate = b_date

    user.Country = request.POST['country']
    user.City = request.POST['city']
    user.State = request.POST['state']
    user.Address = request.POST['address']

    user.save()

    return redirect(profile_page)

# upload profile image
def upload_image(request):
    # print(request.POST, type(request.POST['profile_image']))
    print(request.FILES)
    
    master = Master.objects.get(Email = request.session['email'])
    user = UserProfile.objects.get(Master=master)

    if 'profile_image' in request.FILES:
        user.ProfileImage = request.FILES['profile_image']
    
    user.save()
    
    return redirect(profile_page)

# add education functionality
def add_education(request):
    master = Master.objects.get(Email=request.session['email'])
    user = UserProfile.objects.get(Master=master)
    
    education = Education.objects.create(
        UserProfile = user,
        BoardUniversity = request.POST['board_university'],
        StartDate = request.POST['start_date'],
        EndDate = request.POST['end_date'],
    )

    if 'is_completed' in request.POST:
        education.IsCompleted = True
    
    education.save()

    return redirect(profile_page)

# edit education page
def edit_education_page(request, pk):
    education = Education.objects.get(pk=pk)
    education.StartDate = education.StartDate.strftime("%Y-%m-%d")
    education.EndDate = education.EndDate.strftime("%Y-%m-%d")
    default_data['edit_edu'] = education
    return redirect(profile_page)

# edit education
def edit_education(request, pk):
    education = Education.objects.get(pk=pk)
    education.BoardUniversity = request.POST['board_university']
    education.StartDate = request.POST['start_date']
    education.EndDate = request.POST['end_date']
    
    if 'is_completed' in request.POST:
        education.IsCompleted = True
    else:
        education.IsCompleted = False
        
    education.save()

    if 'edit_edu' in default_data:
        del default_data['edit_edu']

    return redirect(profile_page)

# delete eductaion
def delete_education(request, pk):
    Education.objects.get(pk=pk).delete()
    return redirect(profile_page)

# add experience functionality
def add_experience(request):
    master = Master.objects.get(Email=request.session['email'])
    user = UserProfile.objects.get(Master=master)
    
    experience = Experience.objects.create(
        UserProfile = user,
        JobTitle = request.POST['job_title'],
        Company = request.POST['company'],
        StartDate = request.POST['start_date'],
        EndDate = request.POST['end_date'],
        Description = request.POST['description']
    )

    if 'is_completed' in request.POST:
        experience.IsCompleted = True
    
    experience.save()

    return redirect(profile_page)

# edit education page
def edit_experience_page(request, pk):
    experience = Experience.objects.get(pk=pk)
    experience.StartDate = experience.StartDate.strftime("%Y-%m-%d")
    experience.EndDate = experience.EndDate.strftime("%Y-%m-%d")
    default_data['edit_exp'] = experience
    return redirect(profile_page)

# edit education
def edit_experience(request, pk):
    experience = Experience.objects.get(pk=pk)
    experience.JobTitle = request.POST['job_title']
    experience.Company = request.POST['company']
    experience.StartDate = request.POST['start_date']
    experience.EndDate = request.POST['end_date']
    experience.Description = request.POST['description']

    print(request.POST)
    
    if 'is_completed' in request.POST:
        experience.IsCompleted = True
    else:
        experience.IsCompleted = False
        
    experience.save()

    if 'edit_exp' in default_data:
        del default_data['edit_exp']

    return redirect(profile_page)

# delete eductaion
def delete_experience(request, pk):
    Experience.objects.get(pk=pk).delete()
    return redirect(profile_page)


# add skills
def add_skills(request):
    master = Master.objects.get(Email=request.session['email'])
    user = UserProfile.objects.get(Master=master)

    Skill.objects.create(
        UserProfile = user,
        SkillName = request.POST['skill_name'],
        Level = request.POST['skill_level'],
    )

    return redirect(profile_page)

# delete skill
def delete_skill(request, pk):
    Skill.objects.get(id=pk).delete()

    return redirect(profile_page)

# logout functionality
def logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect(login_page)