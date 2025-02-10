from setuptools import setup

setup(
    name = "ddpm_py",
    version = "0.1.0",
    packages=['dataset', 'dataset', 'models', 'scheduler', 'tools'],
    description = "Creating a module for easier access within the tools"
)


# with open('req.txt') as f:
#     requirements = f.read().splitlines()