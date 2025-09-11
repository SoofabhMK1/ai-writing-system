from sqlalchemy.types import TypeDecorator, TEXT
import json

class JsonEncodedDict(TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)

class StringArray(TypeDecorator):
    """Enables ARRAY storage for SQLite by encoding and decoding on the fly."""
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return ",".join(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return value.split(",")
