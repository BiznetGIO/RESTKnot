import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("dnsagent/__init__.py", "r", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

with open("README.md", "rb") as f:
    readme = f.read().decode("utf-8")

with open("requirements.txt", "rb") as f:
    requirements = f.read().decode("utf-8")

setup(
    name="dnsagent",
    version=version,
    description="RESTKnot agent",
    long_description=readme,
    url="https://github.com/BiznetGIO/RESTKnot",
    author="BiznetGio",
    author_email="support@biznetgio.com",
    license="MIT license",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="restknot",
    include_package_data=True,
    packages=["dnsagent"],
    install_requires=requirements,
    entry_points={"console_scripts": ["dnsagent = dnsagent.cli:main"]},
)
