from io import open

from setuptools import find_packages, setup

with open("rsf/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.strip().split("=")[1].strip(" '\"")
            break
    else:
        version = "0.0.1"

REQUIRES = ["python-dotenv", "pymongo", "opencc-python-reimplemented"]

setup(
    name="rsf",
    version=version,
    description="wikitonary processing utils for build structure that like WordNet",
    author="GYCHEN",
    author_email="gy.chen@gms.nutc.edu.tw",
    maintainer="GYCHEN",
    maintainer_email="gy.chen@gms.nutc.edu.tw",
    url="https://github.com/gy-chen/rfs",
    install_requires=REQUIRES,
    tests_require=["pytest"],
    packages=find_packages(),
    entry_points={"console_scripts": ["rsf-convert=rsf.convert:main_convert"]},
)
