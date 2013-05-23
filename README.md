Simple Naive Bayes Classifier - Python
======================================

Naive Bayes Classifier is an algorithm to classify texts into sets that is always learning.

The most obvious practical use of it is for Email Spam/Ham Detection.

Motivation
----------

There is a really good video piece in Youtube [here](http://www.youtube.com/watch?v=yvDCzhbjYWs) by [Peter Norvig](http://en.wikipedia.org/wiki/Peter_Norvig), Director of Research at Google. He spoke about The Unreasonable Effectiveness of Data.

Another great piece about the algorithm explained in plain English is by [Alexander Nedelcu](https://www.bionicspirit.com/pages/about.html) with his [blog post here](http://bionicspirit.com/blog/2012/02/09/howto-build-naive-bayes-classifier.html).

Implementation
--------------

Before meddling with Python, I translated Alexander's implementation in Ruby to PHP available [here](https://github.com/tistaharahap/Simple-Naive-Bayes-Classifier-for-PHP).

Benchmarking my oven fresh PHP implementation at the time, [Redis](http://redis.io) was the only answer to achieve sub-second results. I tried MySQL and MongoDB before Redis.

External Dependencies
---------------------
- Redis <http://redis.io>
- [Optional - For Data Import only] MySQL Python Connector <http://dev.mysql.com/doc/connector-python/en/index.html>

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
- Redis v2.4.15 compiled from source
- Python v2.7.2

The data sets is as below:
- 1,212 Sets
- 308,607 Keywords

Classifying Time:
- 1 Keyword: 0.0722010135651 second
- 2 Keywords: 0.194036006927 second
- 3 Keywords: 0.35346698761 second

Optimization
------------

The algorithm is optimized only in a macro level at the moment. Need to micro optimize the algorithm especially with Python's tuples, lists and sets. Still finding my way around them.