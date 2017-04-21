import rules


class Rules:
    """
    Implement the "rules" attribute of a model.

    This attribute decouples all business rules for authorization from the
    model class. This allows for thinner models.
    """

    def __init__(self, model=None):
        self.model = model

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        if self.model:
            return self
        return Rules(instance)

    def _test_multilple(self, user, rule_list, reducer):
        """
        Common implementation to test() and test_any()
        """
        test = rules.test_rule
        model = self.model
        return user.is_superuser or \
            reducer(test(rule, user, model) for rule in rule_list)

    def test(self, user, *rules):
        """
        Return True if user has all given permissions.
        """
        return self._test_multilple(user, rules, all)

    def test_any(self, user, *rules):
        """
        Return True if user has any of the given permissions.
        """
        return self._test_multilple(user, rules, any)

    def test_single(self, user, rule):
        """
        Return True if user has permission.
        """
        return user.is_superuser or rules.test_rule(rule, user, self.model)
