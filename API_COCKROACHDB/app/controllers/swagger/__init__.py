import os
from flask_swagger_ui import get_swaggerui_blueprint


# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    # URL for exposing Swagger UI (without trailing '/')
    os.getenv('SWAGGER_URL'),
    # Our API url (can of course be a local resource)
    os.getenv('SWAGGER_API_URL'),
    config={  # Swagger UI config overrides
        'app_name': os.getenv('APP_NAME')
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)
