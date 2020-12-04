from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="text2numde",
    version="1.0",
    author="Jonas Freiknecht",
    author_email="j.freiknecht@googlemail.com",
    description="This library converts German numbers written as text to integer and float values.",
	test_suite="tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/padmalcom/text2numde",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)