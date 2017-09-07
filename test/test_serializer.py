from db import serializer


class DeserializeMe(Serializable):
    def __init__(self, name):
        self.name = name
        self.seiralize_table = {'name_column': 'name'}


def test_deserialize_from():
        result = ['jake'] # SELECT name_column FROM names
        test_class = DeserializeMe(None)
        test_class.deserialize_from(result)
        assert test_class.name == 'jake'

        # Small edge case to deal with
