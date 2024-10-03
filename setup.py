from setuptools import setup, find_packages

setup(
    name='witness-client',
    version='0.1.0',
    description='A Python client for the Witness API',
    long_description=open("README.md", 'r').read(),
    long_description_content_type='text/markdown',
    author='Mihir Wadekar, Joe Coll',
    author_email='team@witness.co',
    url='https://github.com/WitnessCo/client-py',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)