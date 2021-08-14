'''
    People urls.py
'''
from django.conf.urls import url

from . import views

app_name = 'people'

urlpatterns = [
    # people
    url(r'^$', views.index, name='index'),
    url(r'^person/create/$', views.PersonCreate.as_view(), name='create_person'), 
    url(r'^person/(?P<pk>[0-9]+)/$', views.PersonDetail.as_view(), name='person_detail'),
    url(r'^person/(?P<pk>[0-9]+)/update$', views.PersonUpdate.as_view(), name='update_person'),    
    url(r'^person/(?P<pk>[0-9]+)/delete/$', views.PersonDelete.as_view(), name='delete_person'),    
    url(r'^cv/(?P<person_id>[0-9]+)/$', views.person_cv, name='person_cv'),
    # Education
    url(r'^education/$', views.EducationList.as_view(), name='list_education'), 
    url(r'^education/create/$', views.EducationCreate.as_view(), name='create_education'), 
    url(r'^education/(?P<pk>[0-9]+)/$', views.EducationDetail.as_view(), name='education_detail'),
    url(r'^education/(?P<pk>[0-9]+)/update$', views.EducationUpdate.as_view(), name='update_education'),    
    url(r'^education/(?P<pk>[0-9]+)/delete/$', views.EducationDelete.as_view(), name='delete_education'),    
]