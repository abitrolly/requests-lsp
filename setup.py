from setuptools import setup

setup(
    name='requests-lsp',
    version='0.1',
    packages=['requests_lsp'],
    install_requires=['requests>=2.0.0'],
    provides=['requests_lsp'],
    author='Anatoli Babenia',
    author_email='anatoli@rainforce.org',
    url='https://github.com/abitrolly/requests-lsp',
    description='Requests Transport Adapter for Language Server Protocol.',
    license='Unlicense',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: The Unlicense (Unlicense)',
        'Intended Audience :: Developers',
    ],
)
