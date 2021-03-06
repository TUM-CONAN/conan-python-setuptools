import os

from conans import ConanFile, tools


class PythonSetuptoolsConan(ConanFile):
    name = "python-setuptools"
    version = tools.get_env("GIT_TAG", "41.2.0")
    license = "Apache"
    description = ("Easily download, build, install, upgrade, and uninstall Python packages")
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        tools.get("https://github.com/pypa/setuptools/archive/v%s.tar.gz" % self.version)

    def build_requirements(self):
        self.build_requires("generators/1.0.0@camposs/stable")

    def requirements(self):
        self.requires("python/[>=3.8.2]@camposs/stable")

    def build(self):
        py_path = os.path.join(self.package_folder, "lib", "python3.7", "site-packages")
        env = {"PYTHONPATH": py_path}
        os.makedirs(py_path)
        with tools.chdir("setuptools-" + self.version), tools.environment_append(env):
            self.run("python3 bootstrap.py")
            self.run('python3 setup.py install --optimize=1 --prefix= --root="%s"' % self.package_folder)

    def package_info(self):
        self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "lib", "python3.7", "site-packages"))
