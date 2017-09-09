''' Serialize objects into SQLITE database calls. '''


class Serializable:
    ''' Serializable class that implements methods for objects wishing to
    serialize to SQLITE tables. This is done with a serialize table that maps
    property names to SQLITE table columns. When insert_into is called it takes
    the properties listed in serialize table and the corresponding table column
    names, building an SQLITE query to use on the database. '''

    def __init__(self, serialize_table):
        ''' Initialize the Serializable class'''
        self.serialize_table = serialize_table

    def deserialize_from(self, row):
        ''' Deserialize object from the result of an sqlite SELECT call.
        Example:

        >>> class DeserializeMe(Serializable):
        >>>   def __init__(self, name):
        >>>     self.name = name
        >>>     self.seiralize_table = {'name_column': 'name'}
        >>>
        >>> result = ['jake'] # SELECT name_column FROM names
        >>> test_class = DeserializeMe(None)
        >>> test_class.deserialize_from(result)
        >>> assertEquals(test_class.name, 'jake') '''
        properties = [prop for _, prop in self.serialize_table]
        for prop, value in zip(properties, row):
            setattr(self, prop, value)

    def insert_into(self, sqlite_table):
        ''' Serialize object into a sqlite INSERT call.
        Example:
        >>> class SerializeMe(Serializable):
        >>>   def __init__(self, name):
        >>>     self.name = name
        >>>     self.seiralize_table = {'name': 'name'}
        >>>
        >>> test = SerializeMe('jack')
        >>> query = test.insert_into('names')
        >>> assertEquals(query, ('INSERT INTO names (name) VALUES (?)', 'jack')) '''
        keys = ', '.join(column for column, _ in self.serialize_table)
        values = [getattr(self, prop) for _, prop in self.serialize_table]
        placeholders = ', '.join('?' for value in values)
        sqlite_query_format = f'INSERT INTO {sqlite_table} ({keys}) VALUES ({placeholders})'
        return sqlite_query_format, values
