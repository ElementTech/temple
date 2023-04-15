import os
from flask import Flask, render_template
from threading import Thread


class TempleServer(Thread):
    def __init__(self, temple, temple_file):
        super().__init__()
        self.temple = temple
        path = os.path.dirname(temple_file)
        self.app = Flask(__name__, template_folder=os.path.join(path,"templates"),root_path=os.getcwd())
        print(self.app.root_path)
        for param in self.temple.parameters:
            setattr(self.app.config, param.name, param.default)
        rel_path = os.path.relpath(temple.template, path)
        full_path = os.path.join(path, rel_path)
        @self.app.route("/")
        def index():
            template_params = {param.name: getattr(self.app.config, param.name) for param in self.temple.parameters}
            return render_template(full_path, **template_params)

    def run(self):
        self.app.run()

    def update_parameter(self, param_name, value):
        setattr(self.app.config, param_name, value)
