from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, Course, Grade
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from django.db import connection


def index(r):
    return render(r, 'base.html')


# для оптимизации запросов
# select_related	            prefetch_related
# -------------------------------------------------------
# Для ForeignKey и OneToOne	    Для ManyToMany и reverse ForeignKey
# JOIN в SQL	                Отдельные запросы + объединение в Python
# Один сложный запрос	        Несколько простых запросов


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
    # def get(self, r, *args, **kwargs):
    #     f = r.GET.get('f', default='')
    #     # print(f)
    #     # к примеру фильтр на содержание в имени подстроки из параметров в get
    #     # можно на странице сделать поле для фильтра
    #     students = Student.objects.filter(name__contains=f).all()
    #     return render(r, self.template_name, context={'students':students})
    
    
# просмотр одной записи    
class StudentView(DetailView):
    model = Student
    template_name = 'student.html'          
    slug_url_kwarg = 'name_slug'
    context_object_name = 'student'
    # pk_url_kwarg = 'pk' # т.к. тут slug ссылка по id уже не нужна
    # login_url = '/login/'      
    
    
# ----------------------- COURSES
class Courses(ListView):
    model = Course
    template_name = 'courses.html'
    context_object_name = 'courses' 

class Show_course(DetailView):
    model = Course
    template_name = 'course.html'
    pk_url_kwarg = 'id'    