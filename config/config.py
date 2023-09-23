class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///shop.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATION = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://tienda:tienda@localhost/tienda'

class DevelpmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'c43b00a63a652b54e6bd6035b4294253150f481dc4951313d3c2b3f2fcb6'