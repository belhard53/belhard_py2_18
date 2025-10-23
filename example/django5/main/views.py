from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Student, Course, Grade
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView

from django.views.decorators.cache import cache_page

from .forms import *

from django.db import connection


def index(r):
    return render(r, 'base.html')


# для оптимизации запросов
# select_related	            prefetch_related
# -------------------------------------------------------
# Для ForeignKey и OneToOne	    Для ManyToMany и reverse ForeignKey
# JOIN в SQL	                Отдельные запросы + объединение в Python
# Один сложный запрос	        Несколько простых запросов

# @cache_page(60*15)
def students(r):
    # взять всех студентов но при это связи на загрузятся
    # они будут грузиться автоматом при запросе для каждого студента отдельно
    # сколько студентов столько запросов
    # students = Student.objects.all()
    
    # загрузить сразу отдельным запросом курсы из каждого студента
    # 2 запроса при любом количестве данных
    # students = Student.objects.prefetch_related('course').all()
    
    # или к примеру отдельным запросом по цепочке (двойное подчеркивание)
    # студенты -> у студентов оценки -> у оценок ее курс 
    # 3 запроса при любом количестве данных
    students = Student.objects.prefetch_related('grades__course').all()
    # еще более сложная цепочка
    # students = Student.objects.prefetch_related('grades__course__student_set').all()
    
    
    for s in students:
        c = [f'{g.grade} - {g.course}' for g in s.grades.all()]        
        # print(type(c))
        print(s.name, ' - ' , c or 'нет оценок')
        
        
    print('-----------------------')
    print(f"Запросов: {len(connection.queries)}")
    for query in connection.queries:
        print(query['sql'])    
    
    return render(r, 'students.html', 
                    context={'students':students})
    
    
def student(r, id):
    student = Student.objects.get(id=id)    
    return render(r, 'student.html', context={'student':student})    


# ---------------

# список
class StudentsView(ListView):
    model = Student
    template_name = 'students.html'
    context_object_name = 'students'
    
    
    # можно добавить необязательные параметры
    
    # для уточнения запроса если нет "def get"
    # def get_queryset(self) -> QuerySet[Any]:
    #     return Student.objects.filter(name='Вася')
    
    # для добавления в контекст доп данных если нет "def get"
    # def get_context_data(self, **kwargs) -> dict[str, Any]:
    #     context =  super().get_context_data(**kwargs)
    #     context['menu'] = menu
    #     return context
    
    # можно переписать метод обслуживающий get-запрос для 
    # считывания доп параметров
    # http://127.0.0.1:8000/students2/?f=ас
    def get(self, r, *args, **kwargs):
        f = r.GET.get('f', default='')
        print(f)
        # к примеру фильтр на содержание в имени подстроки из параметров в get
        # можно на странице сделать поле для фильтра
        students = Student.objects.filter(name__contains=f).all()
        return render(r, self.template_name, context={'students':students})
    
    
# просмотр одной записи    
class StudentView(DetailView):
    model = Student
    template_name = 'student.html'          
    slug_url_kwarg = 'name_slug'
    context_object_name = 'student'
    # pk_url_kwarg = 'pk' # т.к. тут slug ссылка по id уже не нужна
    # login_url = '/login/'      
    
    
    
# добавить запись
class StudentAddView(LoginRequiredMixin, CreateView): # login дб первый
    form_class = StudentAddForm
    template_name = 'student_add_form.html'
    # template_name = 'student_add_form_manual.html' # тут форма создается вручную
    success_url = reverse_lazy('students')
    login_url = '/login/'


# изменить данные
class StudentEditView(UpdateView):
    model = Student
    fields = '__all__'
    template_name = 'student_edit_form.html'
    pk_url_kwarg = 'id'
    # Если form_class не указан, автоматически создаёт форму на основе  модели
    


# # изменить данные - через функцию
@login_required(login_url='/login/')
def student_edit_view(r, id):    
    student = get_object_or_404(Student, id=id)    
    if r.method=='GET':        
        return render(
                    request=r, 
                    template_name='student_edit_form.html', 
                    context={'form':StudentAddForm(instance=student), 'id':id})
    # POST
    form = StudentAddForm(r.POST, instance=student)
    if form.is_valid(): 
        print(form.cleaned_data)
        form.save()
        return redirect('students')   
    form.add_error(None, "Ошибка....")
    return render(r, 'student_edit_form.html', {'form':form})     





# ----------------------- COURSES
class Courses(ListView):
    model = Course
    template_name = 'courses.html'
    context_object_name = 'courses' 

class Show_course(DetailView):
    model = Course
    template_name = 'course.html'
    pk_url_kwarg = 'id'    





# используя ручную форму    
# def course_add_view(r):

#     if r.method == "POST":
#         form = CourseAddForm(r.POST)        
#         if form.is_valid():        
#             try:                
#                 Course.objects.create(**form.cleaned_data)
#             except Exception as e:
#                 form.add_error(None, "Ошибка ....")
#                 print(e)
#     else:
#         form = CourseAddForm()
#     return render(r, 'course_add_form.html', context={'form':form})

# используя форму основанную на модели ORM
@login_required(login_url='/login/')
def course_add_view(r):
    if r.method == "POST":
        form = CourseAddForm2(r.POST)        
        if form.is_valid():
            form.save()
            return redirect("courses")    
    else:
        form = CourseAddForm2()
    return render(r, 'course_add_form.html', context={'form':form})


class CourseEditView(UpdateView):
    model = Course
    fields = '__all__'    
    template_name = 'course_add_form.html'
    pk_url_kwarg = 'id'
    
    # если не указать success_url будет переходить на страницу этого курса через Course.get_absolute_url()
    # success_url = reverse_lazy('courses')
    
class CourseDeleteView(DeleteView):
    model = Course      
    template_name = 'course_del_confirm.html'    
    success_url = reverse_lazy('courses')







# -----------------------------------

class LoginUser(LoginView):
    form_class = AuthenticationForm 
    template_name = 'login.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('index')

class RegisterUser(CreateView):
    # form_class = UserCreationForm # джанговская формма
    form_class = RegisterUserForm # своя форма на основе джанговой
    template_name = 'reg.html'
    success_url = reverse_lazy('login') # для входа сайта
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')
    
    
def logout_user(r):
    logout(r)
    return redirect('index')    