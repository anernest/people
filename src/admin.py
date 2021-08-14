from django.contrib import admin

# Register your models here.
from address.models import AddressField, Address
from address.forms import AddressWidget
from .models import Person, Organization, Education, License, Appointment, Honor, Relationship

class PersonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        AddressField: {'widget': AddressWidget(attrs={'style': 'width: 300px;'})}
    }
    
admin.site.register(Person, PersonAdmin)
#admin.site.register(Address)

class RelationshipInline(admin.StackedInline):
    model = Relationship
    fk_name = 'from_organization'

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]
    formfield_overrides = {
        AddressField: {'widget': AddressWidget(attrs={'style': 'width: 300px;'})}
    }    

admin.site.register(Education)
admin.site.register(License)
admin.site.register(Appointment)
admin.site.register(Honor)
admin.site.register(Organization, OrganizationAdmin)