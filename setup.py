from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ['psutil']

setup(
    name="pyhacknet",
    version="0.0.1",
    author="Timofey Antonenko",
    author_email="antonenkodev@gmail.com",
    description="A package to convinient usage of networks",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/pyhacknet/pyhacknet",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
