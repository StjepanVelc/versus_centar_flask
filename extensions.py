from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate

migrate = Migrate()
db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)
