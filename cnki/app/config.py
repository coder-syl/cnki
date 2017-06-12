import os

basedir = os.path.abspath(os.path.dirname(__name__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'CgZuaRrkC44hWEkdY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sqlite.db')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://' + 'root:52shangxian' + '@localhost/cnki'
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-testing.db')


class DeployConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    DEBUG = False


config = {
    'default': Config,
    'dev': DevelopmentConfig,
    'testing': TestConfig,
    'deploy': DeployConfig
}
