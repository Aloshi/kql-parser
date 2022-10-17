import re
from setuptools import setup


setup(
    name='kql-parser',
    version=open('VERSION', 'r').read().strip(),
    author='aloshi',
    author_email='alces14@gmail.com',
    license='MIT',
    url='https://github.com/Aloshi/kql-parser',

    install_requires=open('requirements.txt').readlines(),
    extras_require=dict(
        dev=open('requirements-dev.txt').readlines()
    ),

    description='A Python parser for the Kibana Query Language (KQL, also known as Kuery).',
    long_description=open('README.md', 'r').read(),
    keywords=['python', 'kql', 'kibana', 'kuery'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],

    packages=["kql_parser"],
    data_files=[('share/kql-parser', ['README.rst'])],
    entry_points=dict(
        console_scripts=[
            'kql-parser=kql_parser.cli:cli'
        ]
    ),
)
