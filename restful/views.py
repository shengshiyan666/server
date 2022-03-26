from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Module_Instance, Teacher_Module_Rating, User, Professor, Module
# Create your views here.

@api_view(['GET'])
def getModuleDetail(request):
    if request.method == 'GET':
        model_details = Module_Instance.objects.all()

        professors = []

        # Store all professors' name that corresponding the certain module
        # Using professor list to store
        for i in model_details:
            professor = []
            for j in i.teacher_name.values():
                professor.append(j['professor_name'])
            professors.append(professor)
        modulelist = list(model_details.values('name', 'year', 'semester', 'name__module_code'))

        for i in range(len(modulelist)):
            modulelist[i]['taught_by'] = professors[i]
        return Response(modulelist)

@api_view(['GET'])
def Register(request):

    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        email = request.GET.get('email')

        user = User(username=username,password=password,email=email)
        user.save()
        return Response('Register successfully')

@api_view(['POST','GET'])
def Login(request):

    if request.method == 'GET':

        username = request.GET.get('username')
        password = request.GET.get('password')

        # Judge if user exists in the database
        user = User.objects.filter(username=username,password=password).first()
        if user:
            request.session['username'] = user.username
            return Response('successful')
        else:
            return Response('unsuccessful')

@api_view(['GET','POST'])
def Logout(request):
    if request.method == 'GET':
        request.session['username'] = None
        return Response('Logout successfully')

@api_view(['GET'])
def rating(request):
    if request.method == 'GET':

        # Update Teacher_Module_Rating table
        vaules = Module_Instance.objects.all().values('name','teacher_name__professor_id','name__module_code','year','semester')
        for i in vaules:
            professor_id = i['teacher_name__professor_id']
            module_code = i['name__module_code']
            year = i['year']
            semester = i['semester']

            item = Teacher_Module_Rating.objects.filter(module_code=module_code,year=year,semester=semester,teacher_code=professor_id)
            if not item:
                Teacher_Module_Rating(module_code=module_code,year=year,semester=semester,teacher_code=professor_id).save()

        # acquire parameters
        professor_code = request.GET.get('professor_code')
        module_code = request.GET.get('module_code')
        year = request.GET.get('year')
        semester = request.GET.get('semester')
        rating = float(request.GET.get('rating'))

        item = Teacher_Module_Rating.objects.filter(teacher_code=professor_code,module_code=module_code,year=year,semester=semester)

        # Update rating and num_rating fields
        if not item:
            return Response('We can not find the corresponding item')
        else:
            one_rating = item.values()
            num_rating = one_rating[0]['num_rating']
            old_average = one_rating[0]['rating']
            new_average = (rating + num_rating * old_average) / (num_rating + 1)
            print(new_average)
            item.update(num_rating=num_rating+1,rating=new_average)
        return Response('Rating successfully!')

@api_view(['GET'])
def getView(request):
    if request.method == 'GET':

        ratings = Teacher_Module_Rating.objects.all().values()
        list_ratings = []
        list_result = []

        # Calculate the average rating for professors in all modules
        for i in ratings:
            list_ratings.append(i)
        for i in range(len(list_ratings)):
            for j in range(i+1,len(list_ratings)):
                if list_ratings[i]['teacher_code'] == list_ratings[j]['teacher_code']:
                    list_ratings[i]['rating'] = (list_ratings[i]['rating'] * list_ratings[i]['num_rating'] + list_ratings[j]['rating'] * list_ratings[j]['num_rating']) / (list_ratings[i]['num_rating'] + list_ratings[j]['num_rating'])
                    list_ratings[j]['id'] = 0

        # Output Json
        for i in list_ratings:
            if i['id'] != 0:
                i['rating'] = round(i['rating'] + 0.00000000000001)
                del i['id']
                del i['module_code']
                del i['year']
                del i['semester']
                del i['num_rating']
                i['professor'] = Professor.objects.filter(professor_id=i['teacher_code']).values('professor_name')[0]['professor_name']
                list_result.append(i)
        return Response(list_result)

@api_view(['GET'])
def getAverage(request):
    if request.method == 'GET':
        professor_id = request.GET.get('professor_id')
        module_code = request.GET.get('module_code')

        result_list = Teacher_Module_Rating.objects.filter(module_code=module_code,teacher_code=professor_id)

        if not result_list:
            return Response('We can not find the corresponding item')
        else:

            # Calculate the total average
            total_num_rating = 0
            total_rating = 0
            result_dic = {}
            for i in result_list.values():
                total_num_rating += i['num_rating']
                total_rating += (i['num_rating'] * i['rating'])
            average_rating = (total_rating * 0.1) / (total_num_rating * 0.1)

            # Output as Json format
            result_dic['professor_id'] = professor_id
            result_dic['professor_name'] = Professor.objects.filter(professor_id=professor_id).values('professor_name')[0]['professor_name']
            result_dic['module_name'] = Module.objects.filter(module_code=module_code).values('module_name')[0]['module_name']
            result_dic['module_code'] = module_code
            result_dic['average_rating'] = round(average_rating + 0.0000000001)
            return Response(result_dic)










