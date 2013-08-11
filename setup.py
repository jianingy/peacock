# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='peacock',
    version='0.1',
    description='',
    author='',
    author_email='',
    install_requires=[
        "pecan",
        "Jinja2",
        "short-url",
        "sqlalchemy",
        "PIL",
    ],
    test_suite='peacock',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup']),
    entry_points="""
    [pecan.command]
    db_sync = peacock.cmd.db_sync:command
    """
)
