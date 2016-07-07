class Indicator(object):
    def __init__(self, service, id, description):
        self.service = service
        self.id = id
        self.description = description
        self._categories = []

    def add_category(self, category):
        self._categories.append(category)

    @property
    def categories(self):
        return self._categories


class Category(object):
    def __init__(self, id, description, calculator):
        self.id = id
        self.description = description
        self.calculator = calculator

    @property
    def value(self):
        return self.calculator.calculate()


class CategoryCalculator(object):
    def __init__(self):
        pass

    def calculate(self):
        raise NotImplementedError

