# from django.core.exceptions import ValidationError
# from codeschool.tests import *
# from codeschool import models
#
#
# @pytest.fixture
# def syspages(db, scope='session'):
#     from cs_core.models import init_system_pages
#     return init_system_pages()
#
#
# @pytest.fixture
# def page_class(syspages):
#     class TestPage(models.CodeschoolProxyPage):
#         class Meta:
#             proxy = True
#             app_label = 'cs_core'
#     return TestPage
#
#
# @pytest.fixture
# def page(page_class, user):
#     page = page_class(title='title', owner=user, slug='slug')
#     page.save()
#     return page
#
#
# def test_page_initializes_with_no_parameters(page_class):
#     new = page_class()
#
#
# def test_page_requires_only_a_title_parameter_to_save(page_class):
#     new = page_class(title='foo')
#     new.save()
#
#     # Assert do not save without a title
#     new = page_class()
#     with pytest.raises(ValidationError):
#         new.save()
#
#
# def test_name_is_an_alias_to_title_on_page_constructor(page_class):
#     new = page_class(title='foo')
#     assert new.name == 'foo'
#     assert new.title == 'foo'
#
#     new = page_class(name='bar')
#     assert new.title == 'bar'
#     assert new.name == 'bar'
#
#
# def test_page_serialization(db, page):
#     serialized = page.dump_python()
#     assert serialized == dict(
#         {'model/type': 'cs_core.testpage'},
#         id='slug',
#         title='title',
#     )
