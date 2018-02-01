from distutils.core import setup

setup(
    name='citynet',
    version='0.1',
    packages=['citynet', 'citynet.src', 'citynet.src.backend'],
    url='',
    license='',
    author='ASE Group 11',
    author_email='',
    description='Sustainable City Management',
    install_requires=[
        "requests"
    ]
)