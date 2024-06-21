import os

from fastapi import FastAPI
from starlette.templating import Jinja2Templates

app = FastAPI()


def get_template(goods_name: str, template_name: str):
    directory = "templates" + str(os.sep) + goods_name
    templates = Jinja2Templates(directory=directory)
    return templates.get_template(template_name)
