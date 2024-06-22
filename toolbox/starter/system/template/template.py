import os.path

import jinja2
from starlette.templating import Jinja2Templates


def get_template(goods_name: str, template_name: str) -> jinja2.Template:
    real_path = os.path.dirname(os.path.realpath(__file__))
    directory = os.path.join(real_path, goods_name)
    templates = Jinja2Templates(directory=directory)
    return templates.get_template(template_name)
