from abc import abstractmethod
from abc import ABC


class Validator(ABC):
    @abstractmethod
    def validate(self, value: object) -> None:
        pass

    def __set_name__(self, owner: object, name: object) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: object, owner: object) -> object:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: object) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)


class Number(Validator):
    def __init__(self, min_value : int, max_value : int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not type(value) == int:
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be "
                             f"less than {self.min_value} "
                             f"and greater than {self.max_value}")


class OneOf(Validator):
    def __init__(self, options: list[str]) -> None:
        self.options = tuple(options[::])

    def validate(self, value: str) -> None:
        if self.options.count(value) == 0:
            raise ValueError(f"Expected mustard to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(["ketchup", "mayo", "burger"])

    def __init__(
            self,
            buns: int,
            cheese: int,
            tomatoes: int,
            cutlets: int,
            eggs: int,
            sauce: str
    ) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
