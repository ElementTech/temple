import os
from flask import Flask, render_template, request
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
        def index():
            template_params = {(param): vars(self.temple).get(param) for param in vars(self.temple)}
            return render_template(os.path.basename(temple.template), **template_params)
        funcDict = {}
        for name, obj in inspect.getmembers(code):
            if inspect.isfunction(obj):
                if has_temple_endpoint_decorator(obj):
                    funcDict[name] = obj
        @self.app.route("/<task>", methods=["GET", "POST"])
        def invoke_function(task):
            if funcDict.get(task):
                if request.method == "POST":
                    return funcDict.get(task)(**request.values)
                return funcDict.get(task)(**request.args)
        # @self.app.route("/run", methods=["GET", "POST"])
        # def invoke_run():
        #     if request.method == "POST":
        #         return code.run(**request.values)
        #     return code.run(**request.args)

        # @self.app.route("/log", methods=["GET", "POST"])
        # def invoke_log():
        #     if request.method == "POST":
        #         return code.log(**request.values)
        #     return code.log(**request.args)

        # @self.app.route("/res", methods=["GET", "POST"])
        # def invoke_res():
        #     if request.method == "POST":
        #         return code.res(**request.values)
        #     return code.res(**request.args)

    def run(self):
        self.app.run()

    def update_parameter(self, param_name, value):
        setattr(self.app.config, param_name, value)


def has_temple_endpoint_decorator(func):
    return getattr(func, 'endpoint', False)