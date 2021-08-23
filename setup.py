from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in warehouse_management/__init__.py
from warehouse_management import __version__ as version

setup(
	name="warehouse_management",
	version=version,
	description="Maintaing the stocks in warehouse",
	author="Logesh",
	author_email="logeshperiyasamy24@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
