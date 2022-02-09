from setuptools import setup
import pathlib

requirementPath = pathlib.Path(__file__).parent.resolve().joinpath('requirements.txt')
install_requires = [] 
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
        
setup(
    install_requires=install_requires, 
    py_modules=['taxes', ],
    python_requires='>=3.6'
    )