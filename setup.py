# coding=utf-8

from setuptools import setup, find_packages

# Distribute py wheels
# python3 setup.py bdist_wheel sdist
# twine check dist/*
# cd dist
# twine upload * -u __token__ -p pypi-token
# python setup.py install

long_description =""
install_requires =""
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding='utf-8') as r:
    install_requires = r.readlines()


setup(
    name="pyquickwebgui",
    version="0.0.1",
    description="Create desktop applications with Flask/Django/FastAPI/web.py!",
    url="https://github.com/iiixxxiii/pyquickwebgui",
    author="iiixxxiii",
    author_email="iiixxxiii@qq.com",
    license="MIT",
    py_modules=["pyquickwebgui"],
    install_requires=install_requires,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
)
