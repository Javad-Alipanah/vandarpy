#!/usr/bin/env python

import setuptools

# Pinning tenacity as the api has changed slightly which breaks all tests.
application_dependencies = ["api-client>=1.3.1", "tenacity>=5.1.0"]
prod_dependencies = []
test_dependencies = ["pytest", "pytest-env", "pytest-cov", "vcrpy", "requests-mock"]
lint_dependencies = ["flake8", "flake8-docstrings", "black", "isort"]
docs_dependencies = []
dev_dependencies = test_dependencies + lint_dependencies + docs_dependencies + ["ipdb"]
deploy_dependencies = ["api-client"]

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as buf:
    version = buf.read()

setuptools.setup(
    name='vandarpy',
    version=version,
    packages=['vandarpy'],
    description='VandarPay Python Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Javad Alipanah',
    author_email='javadalipanah@gmail.com',
    url='https://github.com/Javad-Alipanah/vandarpy',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.7',
    install_requires=application_dependencies,
    extras_require={
        "production": prod_dependencies,
        "test": test_dependencies,
        "lint": lint_dependencies,
        "docs": dev_dependencies,
        "dev": dev_dependencies,
        "deploy": deploy_dependencies,
    },
    include_package_data=True,
    zip_safe=False,
)
