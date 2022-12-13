from django.forms  import ModelForm, forms
from .models import Task, ahre

class TaskForm (ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        
class correoForm (ModelForm):
    class Meta:
        model =ahre
        fields = ['direccion']