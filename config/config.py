class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///shop.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATION = False

class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://tienda:tienda@localhost/tienda'
    SECRET_KEY = '5e3d937f09a95865e69e2b91920bf642929bb1edbc45f2fbe38eb57fc037aa56'

class DevelpmentConfig(Config):
    DEBUG = True
    SECRET_KEY = '5e3d937f09a95865e69e2b91920bf642929bb1edbc45f2fbe38eb57fc037aa56'
    # SECRET_KEY = '5e3d937f09a95865e69e2b91920bf642929bb1edbc45f2fbe38eb57fc037aa56'
