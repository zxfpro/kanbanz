from setuptools import find_packages, setup

setup(
    name="quickuse",
    version="0.1.1",
    author="zhaoxuefeng",
    author_email=" ",
    description="一个自用的包",
    url="",
    packages=find_packages(),
    install_requires=[
        "pydantic~=2.10.4",
        "pyyaml~=6.0.2",
        "loguru~=0.7.3",

    ],
    python_requires=">=3.10",
)
