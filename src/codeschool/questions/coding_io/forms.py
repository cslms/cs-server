from django.forms import ModelForm
from codeschool.questions.coding_io.models import AnswerKey


class AnswerKeyEditForm(ModelForm):

    class Meta:
        model = AnswerKey
        fields = ['source', 'placeholder']


class AnswerKeyAddForm(ModelForm):

    class Meta:
        model = AnswerKey
        fields = ['language', 'source', 'placeholder']
