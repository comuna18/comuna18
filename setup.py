import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='comuna18',
    version='0.0.6',
    author='Joseph Sierra',
    author_email='joseph.sierra@comuna18.com',
    description='Comuna 18 base build',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Deathpandk/comuna18',
    license='MIT',
    packages=['comuna18'],
    install_requires=[
    	'django',
    	'python-dateutil',
    	'django-crispy-forms',
    	],
)
