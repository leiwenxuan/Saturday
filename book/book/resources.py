from import_export import resources
from .models import Person
class PersonResource(resources.ModelResource):
    class Meta:
        model = Person

from .resources import PersonResource
person_resource = PersonResource()
dataset = person_resource.export()
dataset.csv