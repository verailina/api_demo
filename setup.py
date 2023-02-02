
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))


# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup_params = dict(
    name="apisls",
    version="1.0.0",
    author="Vera Ilina",
    author_email="vvegorova@gmail.com",
    keywords="algorithms",
    package_dir={"": "apisls"},
    packages=find_packages("src"),
    # python_requires=[],
    install_requires=[],  # Optional
)

if __name__ == "__main__":
    setup(**setup_params)