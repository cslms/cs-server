import model_reference

from codeschool import models
from .key_value_pairs import ConfigOptionKeyValuePair, DataEntryKeyValuePair
from .fileformat import ProgrammingLanguage, FileFormat


@model_reference.factory('root-page')
def get_wagtail_root_page():
    return models.Page.objects.get(path='00010001')
