from setuptools import find_packages, setup

VERSION = "2.11.0"

ADAPTERS_ROOT = "src/testit_cli/adapters_api"
ADAPTERS_PACKAGES = ["adapters_api"] + [
    f"adapters_api.{pkg}" for pkg in find_packages(where=ADAPTERS_ROOT)
]
CLI_PACKAGES = [
    pkg for pkg in find_packages(where="src")
    if not pkg.startswith("testit_cli.adapters_api")
]

setup(
    name='testit-cli',
    version=VERSION,
    description='This tool is the command line wrapper of Test IT allowing you to upload the test results in real time '
                'to Test IT',
    long_description=open('README.md', "r").read(),
    long_description_content_type="text/markdown",
    url='https://pypi.org/project/testit-cli/',
    author='Integration team',
    author_email='integrations@testit.software',
    license='Apache-2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    py_modules=['testit_cli'],
    packages=CLI_PACKAGES + ADAPTERS_PACKAGES,
    package_dir={
        '': 'src',
        'adapters_api': ADAPTERS_ROOT,
    },
    install_requires=['validators', 'tqdm', 'click~=8.0.4', 'urllib3>=2.6.0', 'python-dateutil'],
    entry_points={
        'console_scripts': [
            'testit = testit_cli.__main__:console_main'
        ]
    }
)
