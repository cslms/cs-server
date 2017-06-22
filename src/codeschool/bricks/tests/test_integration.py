
import pytest
from codeschool.bricks import *


class TestCards:
    """
    Tests all card components.
    """

    @pytest.fixture
    def cards(self):
        return [simple_card('text1', 'title1'),
                simple_card('text2', 'title2'), ]

    def test_simple_card(self):
        card = simple_card('Title', 'My card.')
        html = str(card)
        assert 'Title' in html
        assert '<p>My card.</p>' in html

    def test_card_container_with_title(self, cards):
        container = card_container(cards, title='title')
        html = container.pretty()
        print(html)
        assert '<aside' in html
        assert 'mdl-cell--3-col' in html
        assert 'mdl-cell--9-col' in html

    def test_card_container_without_title(self, cards):
        container = card_container(cards, title=None)
        html = container.pretty()
        print(html)
        assert '<aside' not in html
        assert 'mdl-cell--12-col' in html


class TestNavbar:
    """
    Test the navbar components.
    """


class TestNavigationComponents:
    """
    Test the cs-head and cs-foot components.
    """
