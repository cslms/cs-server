import pytest
from codeschool.sparta.models import organize_groups 

class TestGroups:
    def test_group_size_correct(self):
        users = {'john': 10, 'paul': 9, 'george': 8, 'ringo': 6}
        assert organize_groups(users, 4) == None

    def test_max_grade_user(self):
         users = {'john': 10, 'paul': 9, 'george': 8, 'ringo': 6}
         assert get_max_grade_user(users)== 'john'