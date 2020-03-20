from os.path import abspath, dirname, join
import pkg_resources
import re
import setuptools


lpath = abspath(dirname(__file__))

with open(join(lpath, 'requirements.txt'), "r") as requirements:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements)
    ]


with open(join(lpath, "README.md"), "r") as fh:
    long_description = fh.read()

with open(join(lpath, "denstatbank/__init__.py"), "rt", encoding="utf8") as f:
    version = re.search(r'__version__\s=\s"(.*?)"', f.read()).group(1)

setuptools.setup(
    name="denstatbank",
    version=version,
    author="Gopakumar Mohandas",
    author_email="gopakumarmohandas@gmail.com",
    description="A Python API wrapper to Statistics Denmark's DataBank API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gmohandas/denstatbank.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. If you
    # do not support Python 2, you can simplify this to '>=3.5' or similar, see
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=3.6',

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=install_requires
)
