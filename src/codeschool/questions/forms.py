from django import forms
from wagtail.wagtailadmin.forms import WagtailAdminPageForm


class QuestionAdminModelForm(WagtailAdminPageForm):
    """
    Create title and short_description fields to make it pass basic validation
    if a import_file is defined.
    """

    def __init__(self, data=None, files=None, instance=None, **kwargs):
        if files and 'import_file' in files:
            file = files['import_file']
            post_data = instance.load_post_file_data(file)
            data = data.copy()
            for field, value in post_data.items():
                if not data[field]:
                    data[field] = value
        super().__init__(data, files, instance=instance, **kwargs)


class PushQuestionForm(forms.Form):
    # FIXME: Temporary hack that should go away!

    filename = forms.CharField(max_length=200)
    contents = forms.CharField(widget=forms.Textarea)
    response_format = forms.ChoiceField(choices=[('html', 'HTML'), ('json', 'JSON')])
    parent = forms.CharField(required=False)
    username = forms.CharField(required=False)
    password = forms.CharField(required=False, widget=forms.PasswordInput)