import os
import setuptools
from setuptools import sic
import yaml

info_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'conf/info.yaml')
with open(info_file, 'r', encoding='utf8') as info_fh:
    info = yaml.load(info_fh, Loader=yaml.FullLoader)

readme_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.md')
with open(readme_file, 'r', encoding='utf8') as readme_fh:
    readme = readme_fh.read()

setuptools.setup(
    name='awstaga',
    description='Python CLI for tagging AWS resources configured in YAML file',
    version=sic(info['version']),
    author='Cliffano Subagio',
    author_email='cliffano@gmail.com',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/cliffano/awstaga',
    keywords=['awstaga', 'aws', 'tag', 'tagging'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
    ],
)
