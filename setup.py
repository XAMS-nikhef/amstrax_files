import setuptools

# Get requirements from requirements.txt, stripping the version tags
with open('requirements.txt') as f:
    requires = [
        r.split('/')[-1] if r.startswith('git+') else r
        for r in f.read().splitlines()]

with open('README.md') as file:
    readme = file.read()

with open('HISTORY.md') as file:
    history = file.read()

setuptools.setup(
    name='amstrax_files',
    version='0.0.0',
    description='Auxiliary strax files and placeholders for XAMS and XAMSL',
    author='Joran Angevaare',
    url='https://github.com/XAMS-nikhef/amstrax_files',
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    install_requires=requires,  # No need for setup_requires and tests_require anymore
    extras_require={
        'dev': [
            'pytest',
            'hypothesis',
            'boltons',
            'flake8',
        ],
    },
    python_requires=">=3.6",
    packages=setuptools.find_packages(),
    scripts=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    zip_safe=False,
)
