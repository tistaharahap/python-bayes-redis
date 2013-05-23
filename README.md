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

Optimization
------------

The algorithm is optimized only in a macro level as of [v0.1.0](https://github.com/tistaharahap/python-bayes-redis/tree/v0.1.0). I am still new in Python and micro optimizations will follow soon.

External Dependencies
---------------------
- Redis <http://redis.io>

Use Examples
------------

Please take a look at [test.py](https://github.com/tistaharahap/python-bayes-redis/blob/master/test.py).