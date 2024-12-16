import os

from conan import ConanFile
from conan.tools.files import copy, get, chdir
from conan.tools.layout import basic_layout
from conan.tools.env import Environment

required_conan_version = ">=1.52.0"



class PythonSetuptoolsConan(ConanFile):
    python_requires = "camp_common/0.5@camposs/stable"
    python_requires_extend = "camp_common.CampPythonBase"

    package_type = 'application'

    name = "python-setuptools"
    version = "75.6.0"
    license = "Apache"
    description = ("Easily download, build, install, upgrade, and uninstall Python packages")

    settings = "os", "arch"

    options = { 
        "python": ["ANY"],
        "python_version": [None, "3.12", ],
        "with_system_python": [True, False],
    }

    default_options = {
        "python": "python3",
        "python_version": "3.12",
        "with_system_python": False,
    }

    def build_requirements(self):
        if not self.options.with_system_python:
            self.requires("cpython/[~{}]".format(self.options.python_version))
            self.build_requires("python-pip/24.3.1@camposs/stable")

    def layout(self):
        basic_layout(self, src_folder="src")

    def generate(self):
        env1 = Environment()
        env1.define("PYTHONPATH", os.path.join(self.package_folder, "lib", f"python{self._python_version}", "site-packages"))
        envvars = env1.vars(self)
        envvars.save_script("py_env_file")

    def package_id(self):
        self.info.clear()

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        with chdir(self, self.source_folder):
            self.run('{0} -m pip install --prefix= --root="{1}" .'.format(self._python_exec, self.package_folder))

    def package_info(self):
        self.runenv_info.append_path("PYTHONPATH", os.path.join(self.package_folder, "lib", f"python{self._python_version}", "site-packages"))
        self.buildenv_info.append_path("PYTHONPATH", os.path.join(self.package_folder, "lib", f"python{self._python_version}", "site-packages"))
