from setuptools import setup, Extension

def readme():
    with open('README.md') as f:
        return f.read()

setup(ext_modules=[Extension("BayesRedis", ["BayesRedis/__init__.c"])],
      name='bayesredis',
      version='1.0.3',
      description='A Simple Naive Bayes Classifier in Python',
      long_description=readme(),
      keywords='bayes naive classifier redis cython',
      url='https://github.com/tistaharahap/python-bayes-redis',
      author='Batista Harahap',
      author_email='batista@bango29.com',
      license='MIT',
      packages=['BayesRedis'],
      setup_requires=['redis>=2.7.0'],
      zip_safe=False)
