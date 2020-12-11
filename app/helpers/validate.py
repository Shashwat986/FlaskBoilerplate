from functools import wraps
from flask import request
import jsonschema

def validate_schema(schema):
    def _validate(f):
        @wraps(f)
        def __decorated(self, *args, **kwargs):
            try:
                jsonschema.validate(instance=request.get_json(), schema=schema)
            except jsonschema.exceptions.ValidationError as e:
                validation_function_name = f.__name__ + '_schema_validation_error'
                if hasattr(self, validation_function_name):
                    return getattr(self, validation_function_name)(e)
                else:
                    raise

            return f(self, *args, **kwargs)

        return __decorated

    return _validate
