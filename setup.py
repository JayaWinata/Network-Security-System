'''
setup.py is an essential part of packaging and distributing Python projects.
It is used by setuptools (or disutils in a older Python versions) to define
the configuration of a project, such as metadata, dependencies, and much more
'''

from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    '''
    This function returns all the package / requirements required by this project
    '''
    requirement_list = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != "-e .":
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found!")

    return requirement_list

'''
Setup the metadata of the project
'''
setup(
    name='NetworkSecurity',
    author='Jaya Winata',
    version='0.0.1',
    packages=find_packages(),
    install_requires=get_requirements()
)