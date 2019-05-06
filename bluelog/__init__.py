import os

from flask import Flask, render_template

from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.extensions import bootstrap, ckeditor, moment, db, mail
from bluelog.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    register_logging()
    register_extensions(app)
    register_blueprints(app)
    register_template_context(app)
    return app


# 工厂函数，指创建其他对象的对象，通常是一个返回其他类的对象的函数或方法
def register_logging(app):
    pass


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_content():
        return dict(db=db)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400


def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='quantity of  categories,default is 10.')
    @click.option('--post', default=50, help='quantity of posts,default is 50.')
    @click.option('--comment', dafault=500, help='quantity of comments,default is 500')
    def forge(category, post, comment):
        """Generates the fake categories,posts,and comments."""
        from bluelog.fakes import fake_admin, fake_categorites, fake_posts, fake_comments

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('generating %d categories...' % category)
        fake_categorites(category)

        click.echo('generating %d posts...' % post)
        fake_posts(post)

        click.echo('generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('done')
