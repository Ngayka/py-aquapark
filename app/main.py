from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: any, owner: any) -> None:
        return instance.__dict__.get(self.name, None)

    def __set_name__(self, owner: any, name: str) -> None:
        self.name = name

    def __set__(self, instance: any, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError

        if not self.min_amount <= value <= self.max_amount:
            raise ValueError
        instance.__dict__[self.name] = value
    pass


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 weight: int,
                 height: int
                 ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    @abstractmethod
    def validate(self, visitor: Visitor) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def validate(self, visitor: Visitor) -> bool:
        try:
            self.age = visitor.age
            self.weight = visitor.weight
            self.height = visitor.height
            return True
        except (TypeError, ValueError):
            return False


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def validate(self, visitor: Visitor) -> bool:
        try:
            self.age = visitor.age
            self.weight = visitor.weight
            self.height = visitor.height
            return True
        except (TypeError, ValueError):
            return False


class Slide:
    def __init__(self, name: any, limitation_class: any) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        validator = self.limitation_class()
        return validator.validate(visitor) \
            if hasattr(validator, "validate") \
            else False
