import pytest
from markio import parse_markio

from codeschool.questions.coding_io.tests.test_models import example, source


@pytest.mark.skip
def test_dump_markio_exports_successfully(db):
    question = example('simple')
    md_source = question.dump_markio()
    md = parse_markio(source('simple.md'))
    assert md_source == md.source()
