import os
from flask import Flask, render_template
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

        # @self.app.route("/init", methods=["POST"])
        # def init():
        #     from self.temple.code import example

    def run(self):
        self.app.run()

    def update_parameter(self, param_name, value):
        setattr(self.app.config, param_name, value)
