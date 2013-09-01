Simple Naive Bayes Classifier - Python
======================================

Naive Bayes Classifier is an algorithm to classify texts into sets that is always learning.

The most obvious practical use of it is for Email Spam/Ham Detection.

Motivation
----------

There is a really good video piece in Youtube [here](http://www.youtube.com/watch?v=yvDCzhbjYWs) by [Peter Norvig](http://en.wikipedia.org/wiki/Peter_Norvig), Director of Research at Google. He spoke about The Unreasonable Effectiveness of Data.

Another great piece about the algorithm explained in plain English is by [Alexander Nedelcu](https://www.bionicspirit.com/pages/about.html) with his [blog post here](http://bionicspirit.com/blog/2012/02/09/howto-build-naive-bayes-classifier.html).

Cython
------

Parts of the code where it is applicable are optimized to leverage Cython Static Typing. The speed bump by doing so are notably significant. Please take a look below for benchmark timings.

How To Develop
--------------

If you are cloning the source code from Github or by downloading from PyPi, please have a look at <code>BayesRedis/__init__.pyx</code> for the main source file.

Implementation
--------------

Before meddling with Python, I translated Alexander's implementation in Ruby to PHP available [here](https://github.com/tistaharahap/Simple-Naive-Bayes-Classifier-for-PHP).

Benchmarking my oven fresh PHP implementation at the time, [Redis](http://redis.io) was the only answer to achieve sub-second results. I tried MySQL and MongoDB before Redis.

External Dependencies
---------------------
- Redis <http://redis.io>
- [Optional - For Data Import only] MySQL Python Connector <http://dev.mysql.com/doc/connector-python/en/index.html>

Installation and Configuration
------------------------------

```bash
$ sudo pip install bayesredis
```

Expecting Redis is installed locally:

```python
from BayesRedis import Classifier

bayes = Classifier({
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0
})
```

The 2 main methods are classify and train like so:

```python
bayes.train('block of text', 'set');
bayes.classify('query')
```

Use Examples
------------

Please take a look at [test.py](https://github.com/tistaharahap/python-bayes-redis/blob/master/test.py) for executing the classifier.

To import data using MySQL, take a look at [test-import-mysql.py](https://github.com/tistaharahap/python-bayes-redis/blob/master/test-import-mysql.py).

Performance
-----------

The gear and spec used to test performance is below:
- Macbook Pro Early 2011
- Intel Core i5 2.3 GHz
- 8 GB PC-10600 DDR3 RAM
- SSD
- Redis v2.6.13 compiled from source
- Python v2.7.2

The data sets is as below:
- 1,212 Sets
- 311,525 Keywords

Classifying Time:
- 1 Keyword - PHP @ 0.01428 second - Python 2.7.2 Mac @ 0.008646 second
- 2 Keywords - PHP @ 0.02171 second - Python 2.7.2 Mac @ 0.012975 second
- 3 Keywords - PHP @ 0.04062 second - Python 2.7.2 Mac @ 0.018261 second
- 65 Keywords - Python 2.7.2 Mac @ 0.342203 second