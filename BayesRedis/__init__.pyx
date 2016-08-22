import redis, math, operator, time
from re import sub

cdef class Classifier(object):
    reds = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }
    namespace = {
        'global': 'bayes-redis',
        'blacklist': 'br-blacklist',
        'words': 'br-words',
        'sets': 'br-sets',
        'cache': 'br-cache',
        'delimiter': '_--%%--_',
        'wordcount': '---count---'
    }

    cdef public int max_str_len
    cdef public int index

    cdef public r

    debug = False

    def __init__(self, args=None):
        if args is not None:
            self.reds['host'] = args['host']
            self.reds['port'] = args['port']
            self.reds['db'] = args['db']

        self.r = redis.ConnectionPool(host=self.reds['host'], port=self.reds['port'], db=self.reds['db'])
        if self.r is None:
            raise Exception('Redis is not properly setup. Check redis configs?')

        self.max_str_len = 2
        self.index = 0

        # Namespacing
        for key in self.namespace:
            if key not in ['global', 'delimiter', 'wordcount']:
                self.namespace[key] = '%s-%s' % (self.namespace['global'], self.namespace[key])

    def __del__(self):
        if self.r:
            self.r.disconnect()

    def classify(self, words, count=10):
        cdef float _start = 0.0

        if self.debug:
            print "Debugging is enabled\n"
            _start = time.time()

        score = {}

        cdef float _start_clean = 0.0
        cdef float _time_clean = 0.0
        if self.debug:
            _start_clean = time.time()
        keywords = self.clean_keywords(words)
        if self.debug:
            _time_clean = time.time() - _start_clean

        cdef float _start_all_sets = 0.0
        cdef float _time_all_sets = 0.0
        if self.debug:
            _start_all_sets = time.time()
        sets = self.get_all_sets()
        if self.debug:
            _time_all_sets = time.time() - _start_all_sets

        cdef float _start_set_word_count = 0.0
        cdef float _time_set_word_count = 0.0
        if self.debug:
            _start_set_word_count = time.time()
        set_word_counts = self.get_set_word_count(sets)
        if self.debug:
            _time_set_word_count = time.time() - _start_set_word_count

        cdef float _start_word_count_from_set = 0.0
        cdef float _time_word_count_from_set = 0.0
        if self.debug:
            _start_word_count_from_set = time.time()
        word_count_from_set = self.get_word_count_from_set(keywords, sets)
        if self.debug:
            _time_word_count_from_set = time.time() - _start_word_count_from_set

        cdef float _start_set_loop = 0.0
        cdef float _time_set_loop = 0.0
        if self.debug:
            _start_set_loop = time.time()

        cdef float prob
        for set in sets:
            for word in keywords:
                key = "%s%s%s" % (word, self.namespace['delimiter'], set)
                if word_count_from_set[key] and word_count_from_set[key] > 0:
                    prob = (float(word_count_from_set[key]) / float(set_word_counts[set]))
                    if not math.isinf(prob) and prob > 0:
                        score[set] = prob
        if self.debug:
            _time_set_loop = time.time() - _start_set_loop

        cdef float _start_sort = 0.0
        cdef float _time_sort = 0.0
        if self.debug:
            _start_sort = time.time()
        ret = sorted(score.iteritems(), key=operator.itemgetter(1), reverse=True)[:count]
        if self.debug:
            _time_sort = time.time() - _start_sort

        cdef float _end = time.time() - _start

        if self.debug:
            print "Debug Statistics"
            print "----------------\n"
            print "Clean Time: %s - %.2f %%" % (_time_clean, (_time_clean/_end*100))
            print "All Sets Time: %s - %.2f %%" % (_time_all_sets, (_time_all_sets/_end*100))
            print "Set Word Count Time: %s - %.2f %%" % (_time_set_word_count, (_time_set_word_count/_end*100))
            print "Word Count From Set Time: %s - %.2f %%" % (_time_word_count_from_set, (_time_word_count_from_set/_end*100))
            print "Set Loop Time: %s - %.2f %%" % (_time_set_loop, (_time_set_loop/_end*100))
            print "Sorting Time: %s - %.2f %%" % (_time_sort, (_time_sort/_end*100))
            print "\nOverall Time: %s\n\n" % _end

        return ret

    def add_to_blacklist(self, word):
        if word and isinstance(word, str):
            self.r.incr("%s#%s" % (self.namespace['blacklist'], word))
        else:
            raise Exception('Can only add strings to blacklist.')

    def remove_from_blacklist(self, word):
        if word and isinstance(word, str):
            self.r.set("%s#%s" % (self.namespace['blacklist'], word), 0)

            # Words
            self.r.hincrby(self.namespace['words'], word, -1)
            self.r.hincrby(self.namespace['words'], self.namespace['wordcount'], -1)
        else:
            raise Exception('Can only remove strings from blacklist.')

    def is_blacklisted(self, word):
        if word and isinstance(word, str):
            res = self.r.get("%s#%s" % (self.namespace['blacklist'], word))
            return not not res
        else:
            raise Exception('Can only check strings from blacklist.')

    def clean_keywords(self, words):
        if isinstance(words, str):
            kws.replace('\n', ' ')
            kws = words.split(" ")
        elif isinstance(words, list):
            kws = words
        else:
            raise Exception('Can only clean String or List.');

        return [sub("[^a-z]", "", kw.lower()) for kw in kws if kw if len(kw) > self.max_str_len]

    def train(self, words, set):
        words = self.clean_keywords(words)
        for word in words:
            self._train_to(word, set)

    def _train_to(self, word, set):
        # Words
        self.r.hincrby(self.namespace['words'], word, 1)
        self.r.hincrby(self.namespace['words'], self.namespace['wordcount'], 1)

        # Sets
        key = "%s%s%s" % (word, self.namespace['delimiter'], set)
        self.r.hincrby(self.namespace['words'], key, 1)
        self.r.hincrby(self.namespace['sets'], set, 1)

    def detrain(self, words, set):
        words = self.clean_keywords(words)
        for word in words:
            self._detrain_from_set(word, set)

    def _detrain_from_set(self, word, set):
        key = "%s%s%s" % (word, self.namespace['delimiter'], set)

        check = (self.r.hexists(self.namespace['words'], word)
                 and self.r.hexists(self.namespace['words'], self.namespace['wordcount'])
                 and self.r.hexists(self.namespace['words'], key)
                 and self.r.hexists(self.namespace['sets'], set))
        if check:
            # Words
            self.r.hincrby(self.namespace['words'], word, -1)
            self.r.hincrby(self.namespace['words'], self.namespace['wordcount'], -1)

            self.r.hincrby(self.namespace['words'], key, -1)
            self.r.hincrby(self.namespace['sets'], set, -1)

            return True
        else:
            return False

    def get_all_sets(self):
        return self.r.hkeys(self.namespace['sets'])

    cdef int get_set_count(self):
        return self.r.hlen(self.namespace['sets'])

    def get_word_count(self, words):
        return self.r.hmget(self.namespace['words'], words)

    cdef int get_all_words_count(self):
        return self.r.hget(self.namespace['wordcount'], self.namespace['wordcount'])

    def get_set_word_count(self, sets):
        if sets:
            ret = {sets[self._next_index()]: self._none_check(v) for v in self.r.hmget(self.namespace['sets'], sets)}
            self.index = 0
            return ret
        else:
            return 0

    def get_word_count_from_set(self, words, sets):
        ret = {}
        if sets:
            keys = ["%s%s%s" % (word, self.namespace['delimiter'], set) for word in words for set in sets]
            tmp = [self._none_check(v) for v in self.r.hmget(self.namespace['words'], keys)]
            ret = {key: tmp[self._next_index()] for key in keys}
            self.index = 0

        return ret

    cdef int _next_index(self):
        i = self.index
        self.index += 1
        return i

    def _none_check(self, v):
        if v is None:
            return 0
        else:
            return int(v)
