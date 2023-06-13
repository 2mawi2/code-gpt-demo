from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

with open('README.md') as f:
    readme = f.read()

long_description = readme

setup(
    name='code-gpt',
    version='1.0.0',
    author='Marius Wichtner',
    author_email='2mawi2@gmail.com',
    url='https://github.com/2mawi/code-gpt',
    description='A smart coding assistant that helps you write code using GPT models',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'codegpt=codegpt.main:main'
        ]
    },
    keywords='code gpt openai gpt3 gpt4 coding assistant',
    install_requires=requirements,
    zip_safe=False
)
