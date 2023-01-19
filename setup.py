import setuptools

PACKAGE_NAME = "json_cfdi"
PACKAGE_DESCRIPTION = "CFDI's expedidos por el SAT (México) de XML a objetos python"
PACKAGE_URL = "https://gitlab.com/workyhr/json_cfdi/"
__version__ = "0.2"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setuptools.setup(
    name=PACKAGE_NAME,
    version=__version__,
    author="Worky HR",
    author_email="opensource@worky.mx",
    description=PACKAGE_DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=PACKAGE_URL,
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=[
        "xmlschema>=1.11",
        "jsonpickle>=2.0",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: Spanish",
        "Topic :: Software Development",
    ],
    python_requires=">=3",
)
