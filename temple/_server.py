import os
from flask import Flask, render_template,send_from_directory, request
from threading import Thread
import sys
import importlib
from time import sleep
import ast
import inspect
import functools

class TempleServer(Thread):
    def __init__(self, temple):
        super().__init__()
        self.temple = temple
        self.app = Flask(__name__, template_folder=os.path.dirname(temple.template), root_path=os.getcwd())
        code = self.temple.code

        @self.app.route("/")
        @self.app.route("/<path:path>")
        def index(path=None):
            template_params = {(param): vars(self.temple).get(param) for param in vars(self.temple)}
            if not path:
                return render_template(os.path.basename(temple.template), **template_params)
            return render_template(path, **template_params)

        funcDict = {}
        for name, obj in inspect.getmembers(code):
            if inspect.isfunction(obj):
                if has_temple_endpoint_decorator(obj):
                    funcDict[name] = obj
        @self.app.route("/code/<task>", methods=["GET", "POST"])
        def invoke_function(task):
            if funcDict.get(task):
                if request.method == "POST":
                    return funcDict.get(task)(**request.values)
                return funcDict.get(task)(**request.args)


    def run(self):
        self.app.run()

    def update_parameter(self, param_name, value):
        setattr(self.app.config, param_name, value)


def has_temple_endpoint_decorator(func):
    return getattr(func, 'endpoint', False)