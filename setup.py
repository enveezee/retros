
from setuptools import setup, find_packages

setup(
    name="retros",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'retros = retros.cli:main',
        ],
    },
)
