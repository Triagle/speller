from db import serializer


class DeserializeMe(serializer.Serializable):
    def __init__(self, name):
        self.name = name
        self.other_property = None
        self.serialize_table = [('name_column', 'name')]


def test_deserialize_from():
    result = ['jake']  # SELECT name_column FROM names
    test_class = DeserializeMe(None)
    test_class.deserialize_from(result)
    assert test_class.name == 'jake'

    # Small edge case to deal with when I pass too many items in the rows
    result = ['jake', 'some extra field']
    test_class.deserialize_from(result)
    assert test_class.name == 'jake'


def test_insert_into():
    test_class = DeserializeMe('test name')
    query, values = test_class.insert_into('test_table')
    assert query == 'INSERT INTO test_table (name_column) VALUES (?)'
    assert values == ['test name']

    # Test case with multiple columns, for determinism in the deserialization process.
    # This is more in case I forget that I shouldn't rely on the ordering of python's
    # dictionaries since their behaviour was only added in 3.6 and is discouraged
    # from being depended on.
    test_class.serialize_table.append(('property_column', 'other_property'))
    test_class.other_property = True
    query, values = test_class.insert_into('test_table')
    assert query == 'INSERT INTO test_table (name_column, property_column) VALUES (?, ?)'
    assert values == ['test name', True]
