from tortoise import Tortoise

from .user import User
from .menu import Menu
from .links import Links
from .site import Site

# Initialize model relationships
Tortoise.init_models(["models"], "models")
