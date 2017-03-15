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