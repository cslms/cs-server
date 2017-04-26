from django.db.models import TextField


class MarkdownField(TextField):

    def __init__(self, **kwargs):
        if 'help_text' not in kwargs:
            kwargs['help_text'] = 'Use *emphasised* or **strong** text, link to <:Another page> or include <:image:An image.jpeg>.'
        super(MarkdownField, self).__init__(**kwargs)

    class Media:
        css = {'all': ('wagtailmarkdown/css/simplemde.min.css', )}
        js = (
            'wagtailmarkdown/js/simplemde.min.js',
            'wagtailmarkdown/js/simplemde.attach.js',
        )
