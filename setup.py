from setuptools import setup, find_packages

setup(
    name='nemo_oauth_plugin',
    version="0.0.5",
    packages=find_packages(exclude=["examples", "tests"]),
    url='https://github.com/Capitains/nemo-oauth-plugin',
    license='GNU GPL',
    author='Bridget Almas',
    author_email='balmas@gmail.com',
    description='OAuth2 Plugin for Nemo',
    test_suite="tests",
    install_requires=[
        "Flask-OAuthlib>=0.9.3",
        "flask_nemo>=1.0.0b1"
    ],
    tests_require=[
        "capitains_nautilus>=0.0.5"
    ],
    include_package_data=True,
    zip_safe=False
)
