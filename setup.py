import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='gaston-backend-ramomar',
    version='0.0.1',
    author='Eduardo Garza',
    author_email='hola@ramomar.dev',
    description='Backend for the gaston project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ramomar/gaston-backend',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
    install_requires=[
        'boto3==1.14.44',
        'banes-ramomar @ git+ssh://git@github.com/ramomar/banes.git@v1.0.0',
    ],
)
