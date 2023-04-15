from copy import deepcopy
import os


class Parameter:
    def __init__(self, name, param_type, default=None, choices=None):
        self.name = name
        self.type = param_type
        self.default = default
        self.choices = choices

    @classmethod
    def from_text(cls, name, default=""):
        return cls(name, "text", default=default)

    @classmethod
    def from_number(cls, name, default=0):
        return cls(name, "number", default=default)

    @classmethod
    def from_single_choice(cls, name, default=None, choices=None):
        if not choices:
            raise ValueError("Single choice parameter must have choices.")
        if default and default not in choices:
            raise ValueError("Single choice parameter default must be one of the choices.")
        return cls(name, "single-choice", default=default, choices=choices)

    @classmethod
    def from_multi_choice(cls, name, default=None, choices=None):
        if not choices:
            raise ValueError("Multi choice parameter must have choices.")
        if default and not all(item in choices for item in default):
            raise ValueError("Multi choice parameter default must be a subset of the choices.")
        return cls(name, "multi-choice", default=default, choices=choices)

    @classmethod
    def from_dict(cls, param_dict):
        param_type = param_dict.get("type")
        name = param_dict.get("name")
        default = param_dict.get("default")
        choices = param_dict.get("choices")

        if param_type == "text":
            return cls.from_text(name, default=default)
        elif param_type == "number":
            return cls.from_number(name, default=default)
        elif param_type == "single-choice":
            return cls.from_single_choice(name, default=default, choices=choices)
        elif param_type == "multi-choice":
            return cls.from_multi_choice(name, default=default, choices=choices)
        else:
            raise ValueError("Invalid parameter type: {}".format(param_type))


class Temple:
    def __init__(self, template_dict, template_file):
        self.name = template_dict.get("name")
        self.template = os.path.join(os.path.dirname(template_file), template_dict.get("template", "temple.html"))
        self.script = os.path.join(os.path.dirname(template_file), template_dict.get("script", "temple.py"))
        self.markdown = os.path.join(os.path.dirname(template_file), template_dict.get("markdown", "README.md"))
        self.parameters = [Parameter.from_dict(param_dict) for param_dict in template_dict.get("parameters", [])]

        if not self.name:
            raise AssertionError("Temple file must contain a name.")
        if not os.path.isfile(self.template):
            raise AssertionError(
                f"Jinja2 file {self.template} could not be found. Provide your temple.yaml a relative path to a jinja2 file."
            )
        if not os.path.isfile(self.script):
            raise AssertionError(
                f"Script file {self.script} could not be found. Provide your temple.yaml with a relative path to the entrypoint file of your script."
            )
