import pytest
from codeschool.sparta.models import organize_groups 

class TestOrganizeGroups:
    def test_groups_user_quantity_less_group_size(self):
        users = {'paul': 9, 'john': 10, 'ringo': 6, 'george': 8}
        expect_groups = [{'john': 10, 'paul': 9, 'george': 8, 'ringo': 6}]
        assert organize_groups(users, 5) == expect_groups

    def test_groups_quantity_of_members(self):
        users = {
            'george': 8, 'italo': 5.5, 'john': 10, 'maria': 4.6,
            'paul': 0, 'bartolomeu': 8, 'eduardo': 1, 'joao': 4.9, 
            'ringo': 6, 'sebastian': 8.5, 'carol': 8
        }
        quantity_users_first = len(organize_groups(users, 5)[0])
        quantity_users_second = len(organize_groups(users, 5)[1])
        assert quantity_users_first == 6
        assert quantity_users_second == 5

    def test_groups_members_expect(self):
        users = {
            'george': 8.5, 'italo': 5.5, 'john': 10, 'maria': 4.6,
            'paul': 0, 'bartolomeu': 8, 'eduardo': 1, 'joao': 4.9
        }
        expect_groups = [
            {'john': 10, 'paul': 0, 'bartolomeu': 8, 'maria': 4.6},
            {'george': 8.5, 'eduardo': 1, 'italo': 5.5, 'joao': 4.9}
        ]
        assert organize_groups(users, 4) == expect_groups

    def test_groups_menbers_remaining_one(self):
        users = {
            'george': 8.5, 'italo': 5.5, 'john': 10, 'maria': 4.6,
            'paul': 0, 'bartolomeu': 8, 'eduardo': 1, 'joao': 4.9, 'barbara': 5
        }
        expect_groups = [
            {'john': 10, 'paul': 0, 'bartolomeu': 8, 'maria': 4.6, 'barbara': 5},
            {'george': 8.5, 'eduardo': 1, 'italo': 5.5, 'joao': 4.9}
        ]
        assert organize_groups(users, 4) == expect_groups
    
    def test_groups_menbers_remaining_two(self):
        users = {
            'george': 8.5, 'italo': 5.5, 'john': 10, 'maria': 4.6, 'hugo': 6,
            'paul': 0, 'bartolomeu': 8, 'eduardo': 1, 'joao': 4.9, 'barbara': 5
        }
        expect_groups = [
            {'john': 10, 'paul': 0, 'bartolomeu': 8, 'maria': 4.6, 'barbara': 5},
            {'george': 8.5, 'eduardo': 1, 'hugo': 6, 'joao': 4.9, 'italo': 5.5}
        ]
        assert organize_groups(users, 4) == expect_groups
    
    