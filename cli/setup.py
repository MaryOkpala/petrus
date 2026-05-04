from setuptools import setup, find_packages

setup(
    name="petrus",
    version="0.1.0",
    description="Petrus — Internal Developer Platform CLI",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "boto3>=1.26",
        "requests>=2.28",
        "pyyaml>=6.0",
        "rich>=13.0",
        "python-dotenv>=1.0"
    ],
    entry_points={
        "console_scripts": [
            "petrus=petrus.main:cli"
        ]
    },
    python_requires=">=3.9"
)
