import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="json-work-proof",
    version="0.1.2",
    author="Alexander Eichhorn",
    author_email="",
    description="JSON Work Proof (JWP) - proof-of-work algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexeichhorn/python-json-work-proof",
    install_requires=[
        #'cryptography>=2.9.0'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)