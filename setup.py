from setuptools import setup
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='KivyGradient',
    version='0.0.3',
    packages=['kivy_gradient'],
    url='https://github.com/kengoon/KivyGradient',
    license='MIT',
    author='kengo',
    author_email='kengoon19@gmail.com',
    description='KivyGradient allows you to add a gradient color to your Kivy Widget',
    install_requires=["kivy"],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
