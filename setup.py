import setuptools

with open('README.rst', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pygfe',
    version='0.1.0',
    author='Thibaut Lamadon',
    author_email='thibaut.lamadon@gmail.com',
    description='Helper functions of Group Fixed Effect',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/tlamadon/pygfe',
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'matplotlib',
        'tqdm',
        'scikit-learn',
        'ConfigArgParse',
        'pytorch',
        'statsmodels'
      ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
