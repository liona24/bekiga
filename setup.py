from setuptools import setup

setup(
    name='bekiga',
    packages=['bekiga'],
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask-PyMongo',
    ],
)

