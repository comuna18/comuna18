import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='c18',
    version='1.1',
    author='Abraham Mercado',
    author_email='abraham@comuna18.com',
    description='Comuna 18 base build',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/comuna18/comuna18',
    license='MIT',
    packages=['comuna18'],
    install_requires=[
        'django',
        'python-dateutil',
        'django-crispy-forms',
        'dango-filters',
    ],
)
