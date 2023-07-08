from connection_pool import get_connection, setup_schema

decInt = lambda s: int(s, base=10)

class DatabaseObject:
    """ Base class for all database objects. """

    table = None
    """ The table name. """

    fields = {
        "id": ("id", decInt),
    }
    """ A map of the fields in the table with format <python_name>: (<db_name>, <type>). """

    @classmethod
    def load_from_db(cls, cursor, id):
        """ Load an object from the database. """
        cursor.execute(f"SELECT * FROM {cls.table} WHERE id = %s", (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return cls.from_row(row)

    @classmethod
    def search_from_db_by_name(cls, cursor, name):
        """ Find an object in the database by name. """
        cursor.execute(f"SELECT * FROM {cls.table} WHERE name LIKE %s", (name,))
        return [cls.from_row(row) for row in cursor.fetchall()]
    
    @classmethod
    def get_all_from_db(cls, cursor):
        """ Find all objects from the database. """
        cursor.execute(f"SELECT * FROM {cls.table}")
        return [cls.from_row(row) for row in cursor.fetchall()]
    
    @classmethod
    def from_row(cls, row):
        """ Create an object from a row. """
        obj = cls()
        for python_name, (db_name, _) in cls.fields.items():
            setattr(obj, python_name, row[db_name])
        return obj
    
    def save(self, cursor):
        """ Save the object to the database. """
        if self.id is None:
            self._insert(cursor)
        else:
            self._update(cursor)
    
    def _insert(self, cursor):
        """ Insert the object into the database. """
        fields = ", ".join(f for f, _ in self.fields.values() if f != "id")
        values = ", ".join("%s" for f, _ in self.fields.values() if f != "id")
        cursor.execute(f"INSERT INTO {self.table} ({fields}) VALUES ({values}) RETURNING id", self._get_values())
        self.id = cursor.fetchone()["id"]
    
    def _update(self, cursor):
        """ Update the object in the database. """
        fields = ", ".join(f"{f} = %s" for f, _ in self.fields.values() if f != "id")
        cursor.execute(f"UPDATE {self.table} SET {fields} WHERE id = %s", self._get_values() + (self.id,))
    
    def _get_values(self):
        """ Get the values of the fields in the order they are stored in the database. Skip the id field. """
        return tuple(getattr(self, python_name) for python_name, _ in self.fields.values() if python_name != "id")
    
    def __init__(self, id=None, **kwargs):
        self.id = id

        for python_name, _ in self.fields.values():
            setattr(self, python_name, kwargs.get(python_name))
    
    def __str__(self):
        return f"{self.__class__.__name__}({', '.join(f'{k}={self.__getattribute__(k)}' for k in self.fields.keys())})"
    
    def __repr__(self):
        return str(self)


class CPA(DatabaseObject):
    table = "cpas"

    fields = {
        "id": ("id", decInt),
        "name": ("name", str),
    }


class Client(DatabaseObject):
    table = "clients"

    fields = {
        "id": ("id", decInt),
        "name": ("name", str),
        "address": ("address", str),
        "income": ("income", decInt),
        "cpa_id": ("cpa_id", decInt),
        "materials_provided_at": ("materials_provided_at", str),
    }


class Assistant(DatabaseObject):
    table = "assistants"

    fields = {
        "id": ("id", decInt),
        "name": ("name", str),
        "cpa_id": ("cpa_id", decInt),
    }


class TaxReturn(DatabaseObject):
    table = "tax_returns"

    fields = {
        "id": ("id", decInt),
        "client_id": ("client_id", decInt),
        "assistant_id": ("assistant_id", decInt),
        "cpa_id": ("cpa_id", decInt),
        "status": ("status", str),
        "filed_at": ("filed_at", str),
        "reviewed_at": ("reviewed_at", str),
    }

    @classmethod
    def search_from_db_by_name(cls, cursor, name):
        """ Find an object in the database by *client* name. """
        cursor.execute(
            """
            SELECT * FROM tax_returns
            INNER JOIN clients ON clients.id = tax_returns.client_id
            WHERE clients.name LIKE %s
            """,
            (name,)
        )
        #print(cursor.fetchall())
        return [cls.from_row(row) for row in cursor.fetchall()]


if __name__ == "__main__":
    with get_connection() as connection:
        setup_schema(connection)
        with connection.cursor() as cursor:
            test = CPA(name="test")
            test.save(cursor)
            import code
            code.interact(local=locals())