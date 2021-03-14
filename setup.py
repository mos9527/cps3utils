import setuptools,cps3utils

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="cps3utils", # Replace with your own username
    version=cps3utils.__version__,
    author="greats3an",
    author_email="greats3an@gmail.com",
    description="Capcom® CP System III ROM hacking utilites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/greats3an/cps3utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],install_requires=[],
    python_requires='>=3.0',
)