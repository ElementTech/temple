import os
from flask import Flask, render_template, request
from threading import Thread
import sys
import importlib


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

        @self.app.route("/run", methods=["GET","POST"])
        def invoke_run():
            return code.run(**request.form)

        @self.app.route("/log", methods=["GET","POST"])
        def invoke_log():
            return code.log(**request.form)

        @self.app.route("/res", methods=["GET","POST"])
        def invoke_res():
            return code.res(**request.form)

    def run(self):
        self.app.run()

    def update_parameter(self, param_name, value):
        setattr(self.app.config, param_name, value)
