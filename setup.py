import codecs
import os
import re

from setuptools import setup


dir_name = os.path.dirname(__file__)

with codecs.open(os.path.join(dir_name, "pytest_graphql_schema", "__init__.py"), encoding="utf-8") as fd:
    VERSION = re.compile(r".*__version__ = ['\"](.*?)['\"]", re.S).match(fd.read()).group(1)

setup(
    name="pytest-graphql-schema",
    description="Get graphql schema as fixture for pytest",
    author="Ted Chen",
    license="MIT license",
    author_email="imaging8896@gmail.com",
    url="https://github.com/imaging8896/pytest-graphql-schema",
    version=VERSION,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ] + [("Programming Language :: Python :: %s" % x) for x in "2.7 3.5 3.6 3.7 3.8".split()],
    install_requires=["pytest>=4.3", "requests", "pyOpenSSL"],
    tests_require=["tox"],
    packages=["pytest_graphql_schema"],
    entry_points={
        "pytest11": [
            "pytest-graphql-schema = pytest_graphql_schema.plugin",
        ],
    },
)
