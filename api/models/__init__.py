from tortoise import Tortoise

from .user import User
from .menu import Menu
from .links import Links

# Initialize model relationships
Tortoise.init_models(["models"], "models")
