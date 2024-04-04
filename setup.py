from setuptools import setup, find_packages

# Function to read the contents of the requirements.txt file
def read_requirements():
    with open('requirements.txt') as req:
        return req.read().strip().split('\n')

setup(
    name='AutomatedBA',
    version='0.1.0',
    packages=find_packages(),
    install_requires=read_requirements(),
    # Add other setup parameters as necessary
)
