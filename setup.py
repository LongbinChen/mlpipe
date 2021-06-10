from setuptools import setup, find_packages
setup(
    name='mlpipe',
    version='0.1.16',
    author='Longbin Chen',
    author_email='lbchen@gmail.com',
    packages=find_packages(exclude=['mlpipe.migrations', 'mlpipe.templatetags']),
    package_data={'':['*.yaml','*.py']},
    scripts=['bin/ml',],
    license='LICENSE',
    url='https://github.com/LongbinChen/mlpipe',
    description='A toolkit to manage machine learning libraries.',
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=[
        "astroid==1.6.1",
        "backports.functools-lru-cache==1.5",
        "configparser==3.5.0",
        "Django==2.2.24",
        "django-bootstrap-ui==0.5.1",
        "django-bootstrap3==9.1.0",
        "django-tag-parser==2.1",
        "dominate==2.1.17",
        "enum34==1.1.6",
        "futures",
        "isort==4.3.3",
        "lazy-object-proxy==1.3.1",
        "mccabe==0.6.1",
        "pycodestyle==2.3.1",
        "pytz==2018.3",
        "PyYAML==3.12",
        "singledispatch==3.4.0.3",
        "six==1.11.0",
        "termcolor==1.1.0",
        "wrapt==1.10.11",
    ],
)
