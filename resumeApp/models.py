from django.db import models

# Create your models here.
# master
# user_profile
# education
# experience
# skills
# projects
# reference

class Master(models.Model):
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=12)
    IsActive = models.BooleanField(default=False)

    is_model = True

    class Meta:
        db_table = 'master'

    def __str__(self) -> str:
        return self.Email

gender_choices = (
    ('m', 'male'),
    ('f', 'female'),
)

class UserProfile(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    ProfileImage = models.FileField(upload_to="profiles/", default='avatar.png')
    FullName = models.CharField(max_length=25, blank=True, null=True)
    UserID = models.CharField(max_length=25, blank=True, null=True)
    Gender = models.CharField(max_length=2, choices=gender_choices)
    BirthDate = models.DateField(default='2000-01-01')
    Country = models.CharField(max_length=25, blank=True, null=True)
    State = models.CharField(max_length=25, blank=True, null=True)
    City = models.CharField(max_length=25, blank=True, null=True)
    Address = models.TextField(max_length=255, blank=True, null=True)

    is_model = True

    class Meta:
        db_table = 'UserProfile'

    def __str__(self) -> str:
        return self.FullName if self.FullName else self.Master.Email

class Education(models.Model):
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    BoardUniversity = models.CharField(max_length=50, blank=True, null=True)
    StartDate = models.DateField(auto_created=True)
    EndDate = models.DateField(auto_created=True)
    IsCompleted = models.BooleanField(default=False)

    is_model = True

    class Meta:
        db_table = 'education'

class Experience(models.Model):
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    JobTitle = models.CharField(max_length=50, blank=True, null=True)
    Company = models.CharField(max_length=50, blank=True, null=True)
    StartDate = models.DateField(auto_created=True)
    EndDate = models.DateField(auto_created=True)
    Description = models.TextField(max_length=500, default=None, blank=True, null=True)
    IsCompleted = models.BooleanField(default=False)

    is_model = True

    class Meta:
        db_table = 'experience'

skill_level = (
    ('begginer', 40),
    ('intermediate', 65),
    ('advance', 100),
)
class Skill(models.Model):
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    SkillName = models.CharField(max_length=25)
    Level = models.IntegerField(choices=skill_level)

    is_model = True

    class Meta:
        db_table = 'skill'


class Project(models.Model):
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ProjectTitle = models.CharField(max_length=50, blank=True, null=True)
    Company = models.CharField(max_length=50, blank=True, null=True)
    StartDate = models.DateField(auto_created=True)
    EndDate = models.DateField(auto_created=True)
    IsCompleted = models.BooleanField(default=False)

    is_model = True

    class Meta:
        db_table = 'project'

class Reference(models.Model):
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=50, blank=True, null=True)
    Company = models.CharField(max_length=50, blank=True, null=True)
    Email = models.EmailField(unique=True)
    Mobile = models.CharField(max_length=10)

    is_model = True

    class Meta:
        db_table = 'reference'