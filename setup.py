#!/usr/bin/env python

from setuptools import setup

setup(
    name='deploy-tix',
    version='0.0.2',
    description='Python scripts for creating deployment tickets in Bugzilla',
    author='Richard Pappalardo',
    author_email='rpappalax@gmail.com',
    url='https://github.com/rpappalax/deploy-tix',
    license="MIT",
    install_requires=['nose >= 1.3.4',
                      'requests >= 2.5.1', \
                      'argparse >= 1.3.0',
                      'httmock >= 1.2.2', \
                      'responses >= 0.3.0'],
    keywords=['deploy', 'deployment', 'services', 'bugzilla'],
    packages=['deploy_tix'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    entry_points={
        'console_scripts':['ticket = deploy_tix.__main__:main']
    },
)
