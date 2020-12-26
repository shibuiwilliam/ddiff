import os
import sys
from glob import glob

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()


def _requires_from_file(filename):
    return open(filename).read().splitlines()


info = sys.version_info

setup(
    name="ddiff",
    version="0.0.2",
    description="diff for structured data",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="shibuiyusuke@gmail.com",
    author_email="shibuiyusuke@gmail.com",
    url="https://github.com/shibuiwilliam/ddiff",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file("requirements.txt"),
    keywords="ddiff",
    entry_points={
        "console_scripts": [
            "ddiff=ddiff.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
)
