from matchers import And, Or, HasAtLeast, HasFewerThan, PlaysIn, All

class QueryBuilder:
    def __init__(self):
        self._matchers = []

    def plays_in(self, team):
        self._matchers.append(PlaysIn(team))
        return self

    def has_at_least(self, value, attr):
        self._matchers.append(HasAtLeast(value, attr))
        return self

    def has_fewer_than(self, value, attr):
        self._matchers.append(HasFewerThan(value, attr))
        return self

    def one_of(self, *queries):
        or_matcher = Or(*queries)
        self._matchers.append(or_matcher)
        return self

    def build(self):
        if not self._matchers:
            return All()
        return And(*self._matchers)
