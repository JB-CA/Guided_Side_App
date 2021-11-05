from os import environ

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        
        URI_VARS = [
            "DB_USER", 
            "DB_PASS", 
            "DB_NAME", 
            "DB_DOMAIN"
        ]

        uri_dict = {item: environ.get(item) for item in URI_VARS}

        for key in URI_VARS:
            if uri_dict[key] is None:
                raise ValueError(f"{key} is not set.")

        return f"postgresql+psycopg2://{uri_dict['DB_USER']}:{uri_dict['DB_PASS']}@{uri_dict['DB_DOMAIN']}/{uri_dict['DB_NAME']}"

class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = True
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True

environment = environ.get("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()