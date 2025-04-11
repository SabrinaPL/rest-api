def validate_fields(data, required_fields):
    """
    Validate that the required fields are present in the data.
    """
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    return True