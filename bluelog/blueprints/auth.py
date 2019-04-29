from flask import Blueprint

# 创建蓝本，用户认证
auth_bp = Blueprint('auth', __name__, static_folder='static', static_url_path='/auth/static')


@auth_bp.route('/login')
def login(user):
    return user


@auth_bp.route('/logout')
def logout():
    return 0
