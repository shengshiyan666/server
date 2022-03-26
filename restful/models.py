from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

# Creating module table
class Module(models.Model):
    module_name = models.CharField(max_length=50,primary_key=True, default=None, blank=False)
    module_code = models.CharField(max_length=10)

    def __str__(self):
        return str(self.module_name)

# Creating Processor table
class Professor(models.Model):
    professor_name = models.CharField(max_length=50)
    professor_id = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return str(self.professor_name)

# Creating module instance table
class Module_Instance(models.Model):

    # Set foreignkey to connect to the module
    name = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(2)])

    # One module instance name can with many professors, one professor can with many module instances
    teacher_name = models.ManyToManyField(Professor)

    def __str__(self):
        name_str = self.teacher_name.all()
        result = ''
        for i in range(len(name_str)):
            if i != len(name_str) -1:
                result += (' ' + str(name_str[i]) + ' and')
            else:
                result += (' ' + str(name_str[i]))
        return str(self.name)+ ', Semester' + str(self.semester) + ', ' + str(self.year) + \
               ', Taught by:' + str(result)

# Record the rating
class Teacher_Module_Rating(models.Model):
    module_code = models.CharField(max_length=10)
    year = models.IntegerField()
    semester = models.IntegerField()
    teacher_code = models.CharField(max_length=10)
    num_rating = models.IntegerField(default=0)
    rating = models.FloatField(default=0)

# Record client registered user
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    email = models.EmailField(default=None)
