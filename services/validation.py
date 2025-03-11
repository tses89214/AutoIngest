from datetime import datetime, date
def validate_schema(preview, schema):
    """
    Validates the schema of a CSV preview against an expected schema.

    Args:
        preview (list): A list of lists representing the CSV preview, including the header row.
        schema (dict): A dictionary representing the expected schema, with column names as keys and data types as values (int, str, float).

    Returns:
        tuple: Returns (True, None) if the schema is valid, otherwise returns (False, error_message).
    """
    header = preview[0]
    if len(header) != len(schema):
        return False, f"Schema does not match: Expected {len(schema)} columns, but got {len(header)} columns"

    expected_col_names = list(schema.keys())
    expected_col_types = list(schema.values())

    for i, col in enumerate(header):
        expected_col_name = expected_col_names[i]
        expected_col_type = expected_col_types[i]
        if col.strip() != expected_col_name:
            return False, f"Schema does not match: Expected column '{expected_col_name}' at position {i+1}, but got '{col}'"

        # Check type of data in preview rows (skip header row)
        for row in preview[1:]:
            value = row[i]
            try:
                if expected_col_type == 'int':
                    if not value.isdigit():
                        return False, f"Schema does not match: Column '{col}' should be of type 'int', but got '{value}'"
                elif expected_col_type == 'str':
                    if not isinstance(value, str):
                        return False, f"Schema does not match: Column '{col}' should be of type 'str', but got '{value}'"
                elif expected_col_type == 'float':
                    if not value.replace('.', '', 1).isdigit():
                        return False, f"Schema does not match: Column '{col}' should be of type 'float', but got '{value}'"
                elif expected_col_type == 'timestamp':
                    try:
                        datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except ValueError:
                        return False, f"Schema does not match: Column '{col}' should be of type 'timestamp', but got '{value}'"
                elif expected_col_type == 'date':
                    try:
                        date.fromisoformat(value)
                    except ValueError:
                        return False, f"Schema does not match: Column '{col}' should be of type 'date', but got '{value}'"
            except Exception as e:
                return False, f"Error during validation: {e}"
    return True, None
