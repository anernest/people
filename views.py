'''
    People views.py
'''
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
'''
    People views.py
'''
from .models import Person, Education, License, Appointment, Honor
from .forms import PersonForm
from django.views import generic
from django.http import HttpResponseForbidden
from django.core.urlresolvers import reverse_lazy
# https://docs.djangoproject.com/en/1.10/topics/class-based-views/intro/#decorating-class-based-views
# https://stackoverflow.com/questions/11774647/use-staff-member-required-decorator-but-without-being-redirected-to-the-admin-i
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required 


def index(request):
    if request.user.is_authenticated():
        person_list = Person.objects.all().order_by('last_name')
    else:
        person_list = {}
    context = {'person_list': person_list}
    return render(request, 'people/index.html', context)

class PersonList(generic.ListView):
    model = Person   

@method_decorator(staff_member_required, name='dispatch')
class PersonCreate(generic.CreateView):
    model = Person  
    fields = '__all__'
    success_url = reverse_lazy('people:index')
    
class PersonDetail(generic.DetailView):
    model = Person   
    
@method_decorator(staff_member_required, name='dispatch')
class PersonDelete(generic.DeleteView):
    model = Person
    success_url = reverse_lazy('people:index')
    
@method_decorator(staff_member_required, name='dispatch')
class PersonUpdate(generic.UpdateView):
    model = Person  
    fields = '__all__'
    success_url = reverse_lazy('people:index')
    
def person_cv(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    education = Education.objects.filter(student=person_id)
    license = License.objects.filter(licensee=person_id)
    appointments = Appointment.objects.filter(incumbent=person_id)
    honor = Honor.objects.filter(honoree=person_id)
    return render(request, 'people/cv.html', {'person': person, 'appointments': appointments, 'education': education, 'license':license, 'honor': honor})

@method_decorator(staff_member_required, name='dispatch')
class EducationCreate(generic.CreateView):
    model = Education  
    fields = '__all__'
    success_url = reverse_lazy('people:index')

class EducationList(generic.ListView):
    model = Education   

class EducationDetail(generic.DetailView):
    model = Education   
    
@method_decorator(staff_member_required, name='dispatch')
class EducationDelete(generic.DeleteView):
    model = Education
    success_url = reverse_lazy('people:index')
    
@method_decorator(staff_member_required, name='dispatch')
class EducationUpdate(generic.UpdateView):
    model = Education  
    fields = '__all__'
    success_url = reverse_lazy('people:index')
    
# def people(request):
    # people = Person.objects.all().order_by('name')
    # context = {'people': people}
    # return render(request, 'curricula/people/index.html', context)
    
# def person(request, person_id):
    # person = get_object_or_404(Person, pk=person_id)   
    # context = {'person': person}
    # return render(request, 'people/person/index.html', context)
    
def can_edit(user):
# Set True if user can edit.
    if user.is_staff or user.is_superuser or user.groups.filter(name='Editor').exists():
        return True
    return False
