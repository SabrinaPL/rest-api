ACCOUNT_CUSTOM_STATUS_CODES = {
  400: {
    "missing_data": "Missing required data in the request body",
    "invalid_data": "Invalid or improperly formatted data",
    "invalid_credentials": "Invalid credentials",
    "missing_first_name": "First name is required and cannot be empty",
    "invalid_first_name": "First name must be a string",
    "missing_last_name": "Last name is required and cannot be empty",
    "invalid_last_name": "Last name must be a string",
    "missing_username": "Username is required and cannot be empty",
    "invalid_username": "Username must be a string",
    "invalid_email": "Invalid email address",
    "invalid_password": "Password is required and must be at least 8 characters long",
    "missing_fields": "Missing required fields in the request body",
    "missing_access_token": "Access token is required in the Authorization header",
    "missing_refresh_token": "Refresh token is required in the Authorization header",
  },
  401: {
    "unauthorized": "Invalid or expired token",
  },
  404: {
    "user_not_found": "User not found with the given credentials",
  },
  500: {
    "internal_error": "An unexpected error occurred while processing the request",
  }
}

USER_CUSTOM_STATUS_CODES = {
  400: {
    "missing_user_id": "User ID is required",
  },
  404: {
    "user_not_found": "User not found",
  },
  500: {
    "internal_error": "An unexpected error occurred while processing the request",
  }
}

MOVIE_CUSTOM_STATUS_CODES = {
  400: {
    "missing_data": "Missing required data in the request body",
    "invalid_data": "Invalid data in the request body",
    "invalid_query": "Invalid query parameters",
    "missing_id": "Missing movie ID in the request",
    "invalid_id": "Invalid movie ID format",
    "invalid_pagination": "Invalid pagination parameters",
    "missing_access_token": "Access token is required in the Authorization header",
  },
  404: {
    "movie_not_found": "Movie not found",
    },
  500: {
    "internal_error": "An unexpected error occurred while processing the request",
  }
}

GENDER_DATA_CUSTOM_STATUS_CODES = {
  400: {
    "invalid_pagination": "Invalid pagination parameters",
    "invalid_query": "Invalid query parameters",
    "invalid_id": "Invalid movie ID format"
  },
  404: {
    "no_gender_data_found": "No gender statistics data found",
  },
  500: {
    "internal_error": "An unexpected error occurred while processing the request",
  }
}

RATING_CUSTOM_STATUS_CODES = {
  400: {
    "invalid_pagination": "Invalid pagination parameters",
    "invalid_query": "Invalid query parameters",
    "invalid_id": "Invalid movie ID format",
  },
  404: {
    "movie_not_found": "Movie not found",
    "no_ratings": "No ratings found",
  },
  500: {
    "internal_error": "An unexpected error occurred while processing the request",
  }
}

CREDIT_CUSTOM_STATUS_CODES = {
  400: {
    "invalid_pagination": "Invalid pagination parameters",
    "invalid_query": "Invalid query parameters for credit filtering",
  },
  404: {
    "no_credits_found": "No credits found matching the given filters",
    "no_actors_found": "No actors found for the specified movie",
    "movie_not_found": "Movie not found while resolving actor credits",
  },
  500: {
    "internal_error": "An unexpected error occurred while processing the request",
  }
}

QUERY_CUSTOM_STATUS_CODES = {
  400: {
    "missing_query": "No query parameters provided",
    "invalid_query": "Invalid query parameters",
    "invalid_rating_value": "Rating filter must be a number between 0 and 5",
    "invalid_year_value": "Year filter must be between 1900 and the current year",
    "invalid_movie_value": "Movie filter must be a string",
    "invalid_actor_value": "Actor filter must be a string",
    "invalid_genre_value": "Genre filter must be a string",
    "invalid_description_value": "Description filter must be a string",
  },
  500: {
    "internal_error": "An unexpected error occurred while processing the request",
  }
}

GENERAL_CUSTOM_STATUS_CODES = {
  500: {
    "internal_error": "An unexpected error occurred while processing the request",
  }
}

JWT_CUSTOM_STATUS_CODES = {
  401: {
    "unauthorized": "Access denied. Invalid or expired token.",
  },
  500: {
    "internal_error": "An unexpected error occurred while processing the request",
  }
}
  