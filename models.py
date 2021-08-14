from django.db import models
import os
#from django_image_tools.models import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.
from address.models import AddressField

# https://groups.google.com/forum/#!topic/django-auth-ldap/GVoa82bLfAE
# from django_auth_ldap.backend import populate_user 

# def make_staff(sender, user, **kwargs): 
    # user.is_staff = True 

# populate_user.connect(make_staff) 

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class Person(models.Model):
    # link to authorized user
    prefix = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    suffix = models.CharField(max_length=30, blank=True, null=True)
    credentials = models.CharField(max_length=30, blank=True, null=True)
    address = AddressField(blank=True, null=True)
#    picture2 = models.ForeignKey(Image, blank=True, null=True)
#    picture = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    avatar_thumbnail = ImageSpecField(source='avatar', processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 60})
    def __str__(self):
        person_string = self.last_name
        if self.first_name:
            person_string += ", " + self.first_name
        if self.middle_name:
            person_string += " " + self.middle_name
        if self.suffix:
            person_string += ", " + self.suffix
        if self.credentials:
            person_string += ", " + self.credentials
        return person_string

class Organization(models.Model):
	name  = models.CharField(max_length=200)
	abbreviation = models.CharField(max_length=20, null=True)
	relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False, related_name='related_to')
	address = AddressField(blank=True, null=True)
	def __str__(self):
		return '/'.join([str(i) for i in self.get_parents()]) + " " + self.name
	# def get_relationships(self, type):
		# return self.relationships.filter(to_organizations__type=type, to_organizations__from_organization=self)
	def get_related_to(self, type):
		return self.related_to.filter(from_organizations__type=type, from_organizations__to_organization=self)
	# def get_children(self):
		# return self.get_relationships(RELATIONSHIP_PARENT)
	def get_parents(self):
		return self.get_related_to(RELATIONSHIP_PARENT)
		
RELATIONSHIP_PARENT = 1
RELATIONSHIP_AGREEMENT = 2
RELATIONSHIP_TYPES = (
    (RELATIONSHIP_PARENT, 'Parent'),
    (RELATIONSHIP_AGREEMENT, 'Agreement'),
)

class Relationship(models.Model):
    from_organization = models.ForeignKey(Organization, related_name='from_organizations')
    to_organization = models.ForeignKey(Organization, related_name='to_organizations')
    type = models.IntegerField(choices=RELATIONSHIP_TYPES)

class Education(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="student")
    advisor = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="advisor", blank=True, null=True)
    start_date = models.DateField('start date')
    end_date = models.DateField('end date', blank=True, null=True)
    institution = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, related_name="institution")
    department = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, related_name="education_department")
    degree = models.CharField(max_length=200, blank=True, null=True)
    major = models.CharField(max_length=200, blank=True, null=True)
    thesis_type = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Thesis, Dissertation, etc")
    thesis_title = models.CharField(max_length=200, blank=True, null=True, help_text="Title of Thesis or Dissertation, etc")
    # Remember to require if in formfield...
    description = models.TextField('description', blank=True, null=True)
    def __str__(self):
        education_string = self.student.__str__() + ", " + self.start_date.strftime('%m/%d/%Y') + "-"
        if self.end_date:
            education_string += self.end_date.strftime('%m/%d/%Y') + ". "
        else:
            education_string += "Current. " 
        if self.degree:
            education_string += self.degree + ", "
        if self.major:
            education_string += self.major + ", "
        if self.department.name:
            education_string += self.department.name + ", "
        if self.institution.name:
            education_string += self.institution.name
        return education_string

class License(models.Model):
    licensee = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="licensee")
    start_date = models.DateField('start date')
    end_date = models.DateField('end date', blank=True, null=True)
    licensor = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, related_name="licensor")
    department = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True,  related_name="licensing_department")
    license_name = models.CharField(max_length=200, blank=True, null=True)
    license_abbreviation = models.CharField(max_length=20, blank=True, null=True)
    license_id = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField('description', blank=True, null=True)
    def __str__(self):
        license_string = self.licensee.__str__() + ", " + self.start_date.strftime('%m/%d/%Y') + "-"
        if self.end_date:
            license_string += self.end_date.strftime('%m/%d/%Y') + ". "
        else:
            license_string += "Current. " 
        if self.license_name:
            license_string += self.license_name + ", "
        if self.license_id:
            license_string += self.license_id + ", "
        if self.department:
            license_string += self.department.name + ", "
        if self.licensor.name:
            license_string += self.licensor.name
        return license_string

class Appointment(models.Model):
	incumbent = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="incumbent")
	supervisor = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="supervisor", blank=True, null=True)
	start_date = models.DateField('start date')
	end_date = models.DateField('end date', blank=True, null=True)
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, related_name="organization")
	department = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, related_name="department")
	rank = models.CharField(max_length=200, blank=True, null=True)
	position = models.CharField(max_length=200, blank=True, null=True)
	description = models.TextField('description', blank=True, null=True)
	ACADEMIC = "academic"
	PROFESSIONAL = 'professional'
	RESEARCH = 'research'
	APPOINTMENT_TYPE_CHOICES = (
		(ACADEMIC, "Academic"),
		(PROFESSIONAL, 'Professional Practice'),
		(RESEARCH, 'Research'),
	)
	appointment_type = models.CharField(max_length=12, choices=APPOINTMENT_TYPE_CHOICES, default=ACADEMIC)
	def __str__(self):
		appointment_string = self.incumbent.__str__() + ", " + self.start_date.strftime('%m/%d/%Y') + "-"
		if self.end_date:
			appointment_string += self.end_date.strftime('%m/%d/%Y') + ". "
		else:
			appointment_string += "Current. " 
		if self.rank:
			appointment_string += self.rank + ", "
		if self.position:
			appointment_string += self.position + ", "
		if self.department.name:
			appointment_string += self.department.name + ", "
		if self.organization.name:
			appointment_string += self.organization.name
		return appointment_string
		
class Honor(models.Model):
    honoree = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="honoree")
    date = models.DateField('date')
    honoror = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, related_name="honoror")
    department = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True,  related_name="honoring_department")
    honor_name = models.CharField(max_length=200, blank=True, null=True)
    honor_abbreviation = models.CharField(max_length=20, blank=True, null=True)
    honor_id = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField('description', blank=True, null=True)
    def __str__(self):
        honor_string = self.honoree.__str__() + ", " + self.honor_name + ", " + self.date.strftime('%m/%d/%Y') + "-" 
        if self.honoror.name:
            honor_string += self.honoror.name
        return honor_string