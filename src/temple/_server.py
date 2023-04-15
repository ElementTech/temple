import os
from flask import Flask, render_template
from threading import Thread


class TempleServer(Thread):
    def __init__(self, temple):
        super().__init__()
        self.temple = temple
        self.app = Flask(__name__, template_folder="./examples/templates")
        for param in self.temple.parameters:
            setattr(self.app.config, param.name, param.default)

        @self.app.route("/")
        def index():
            template_params = {param.name: getattr(self.app.config, param.name) for param in self.temple.parameters}
            return render_template(temple.template, **template_params)

    def run(self):
        self.app.run()

    def update_parameter(self, param_name, value):
        setattr(self.app.config, param_name, value)
