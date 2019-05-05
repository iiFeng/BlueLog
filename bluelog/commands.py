def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='quantity of  categories,default is 10.')
    @click.option('--post', default=50, help='quantity of posts,default is 50.')
    @click.option('--comment', dafault=500, help='quantity of comments,default is 500')
    def forge(category, post, comment):
        """Generates the fake categories,posts,and comments."""
        from bluelog.fakes imports
        fake_admin, fake_categorites, fake_posts, fake_comments

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
