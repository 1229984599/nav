import sys
from pathlib import Path

from dotenv import load_dotenv

# 加载环境变量配置
root_dir = Path(__file__).resolve().parent.parent
load_dotenv(str(root_dir.joinpath('settings', '.env')))

from settings import settings

# 把 core 目录加入到环境变量，主要是 tortoise 的 router 配置必须是 module.class
sys.path.insert(1, str(settings.BASE_PATH.joinpath('core')))
