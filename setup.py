#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['beautifulsoup4>=4.9.1',
                'pandas>=1.0.3',
                'requests>=2.23.0',
                'lxml>=4.5.1']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Himanshu Joshi",
    author_email='hihi.joshi@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Toolset to download variants data from LOVD",
    entry_points={
        'console_scripts': [
            'lovd_tx_map=lovd_downloader.tx_map_cli:main',
            'lovd_variants=lovd_downloader.var_cli:main'
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='lovd_downloader',
    name='lovd_downloader',
    packages=find_packages(include=['lovd_downloader', 'lovd_downloader.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/h-joshi/lovd_downloader',
    version='0.1.0',
    zip_safe=False,
)
