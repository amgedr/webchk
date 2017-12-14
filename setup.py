from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    name='webchk',
    version='0.2.0',
    packages=['webchk'],
    test_suite='test',
    url='https://github.com/amgedr/webchk',
    license="MIT license",
    author='Amged Rustom',
    author_email='amgadhs@codehill.com',
    description='A command-line tool for checking HTTP status codes and response headers of URLs',
    long_description=readme + '\n\n' + history,
    keywords='webchk site management www http link check',
    zip_safe=False,
    include_package_data=False,

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],

    entry_points={
        'console_scripts': [
            'webchk = webchk.__main__:main',
        ]
    },
)
