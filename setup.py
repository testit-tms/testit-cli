from setuptools import find_packages, setup

setup(
    name='testit-cli',
    version='0.1.3',
    description='This tool is the command line wrapper of Test IT allowing you to upload the test results in real time '
                'to Test IT',
    long_description=open('README.md', "r").read(),
    long_description_content_type="text/markdown",
    url='https://pypi.org/project/testit/',
    author='Integration team',
    author_email='integrations@testit.software',
    license='Apache-2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    py_modules=['testit_cli'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['testit-api-client>=3,<4', 'validators', 'tqdm'],
    entry_points={
        'console_scripts': [
            'testit = testit_cli.__main__:console_main'
        ]
    }
)
