from setuptools import setup

setup(
    name = 'session',
    version = '0.1.1',
    packages = ['session'],
    entry_points = {
        'console_scripts': [
            'session = session.__main__:main'
        ]
    }
)
