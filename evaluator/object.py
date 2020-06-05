from dataclasses import dataclass


class ObjTypes:
    INTEGER = "Integer"
    BOOLEAN = "Boolean"
    NULL_OBJ = "Null"


class Object:
    def __str__(self):
        pass

    def type(self) -> str:
        pass


@dataclass
class Integer(Object):
    value: int

    def __str__(self):
        return f"{self.value}"

    def type(self) -> str:
        return ObjTypes.INTEGER


@dataclass
class Boolean(Object):
    value: bool

    def __str__(self):
        return f"{self.value}"

    def type(self) -> str:
        return ObjTypes.BOOLEAN


class Null(Object):
    def type(self) -> str:
        return ObjTypes.NULL_OBJ

    def __str__(self):
        return "null"
