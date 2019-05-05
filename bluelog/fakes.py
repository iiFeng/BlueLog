from bluelog.models import Admin, Category, Post
from bluelog.extensions import db
from faker import Faker


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='bluelog',
        blog_sub_title='hhh',
        name='MiMa Kirigoe',
        about='I,MiMa,had a fun time as a member of CHAM'
    )
    admin.set_password('helloflask')
    db.session.add(admin)
    db.session.commit()


fake = Faker()


def fake_categorites(count=10):
    category = Category(name='Default')  # 创建一个默认分类
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())  # 创建随机分类
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:  # 分类名不能重复，若重复则会导致数据库异常，并抛出异常
            db.session.rollback()  # 进行回滚操作


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake().sentence(),
            body=fake().text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=50):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            reviewed=True,
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # 未审核评论
        comemt = Coment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            reviewed=False,
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    # 管理员发布的评论
    comment = Coment(
        author='Mima',
        email='mima@example',
        site='example.com',
        body=fake.sentence(),
        reviewed=True,
        timestamp=fake.date_time_this_year(),
        post=Post.query.get(random.randint(1, Post.query.count()))
    )
    db.session.add(comment)


db.session.commit()

# 回复
for i in range(salt):
    comment = Coment(
        author=fake.name(),
        email=fake.email(),
        site=fake.url(),
        body=fake.sentence(),
        reviewed=True,
        replied=Comment.query.get(random.randint(1, Comment.query.count())),
        timestamp=fake.date_time_this_year(),
        post=Post.query.get(random.randint(1, Post.query.count()))
    )
    db.session.add(comment)
db.session.commit()
