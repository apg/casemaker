from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='casemaker',
    version='0.1',
    description='casemaker makes test cases',
    long_description=open('README').read(),
    author='Andrew Gwozdziewycz',
    author_email='git@apgwoz.com',
    license='LGPL',
    url='http://github.com/apgwoz/casemaker',
    packages=find_packages(),
    provides=['casemaker'],
    include_package_data=True,
    zip_safe=True,
    requires=[]
)
