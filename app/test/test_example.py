import pytest

class Student:
    def __init__(self, name: str, age: int, major: str):
        self.name = name
        self.age = age
        self.major = major

@pytest.fixture
def default_student():
    return Student('Luiz Santos', 35, 'Information Technology')

def test_student(default_student):
    assert default_student.name == 'Luiz Santos'
    assert default_student.age == 35
    assert default_student.major == 'Information Technology'
