import redis, math, operator
from re import sub

class Classifier():
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
    max_str_len = 2
    r = None

    def __init__(self, args=None):
        if args is not None:
            self.reds['host'] = args['host']
            self.reds['port'] = args['port']
            self.reds['db'] = args['db']

        self.r = redis.StrictRedis(host=self.reds['host'], port=self.reds['port'], db=self.reds['db'])
        if self.r is None:
            raise Exception('Redis is not properly setup. Check redis configs?')

        # Namespacing
        for key in self.namespace:
            if key not in ['global', 'delimiter', 'wordcount']:
                self.namespace[key] = '%s-%s' % (self.namespace['global'], self.namespace[key])

    def classify(self, words, count=10):
        score = {}
        psets = {}

        keywords = self.clean_keywords(words)
        sets = self.get_all_sets()

        set_word_counts = self.get_set_word_count(sets)
        word_count_from_set = self.get_word_count_from_set(keywords, sets)

        for set in sets:
            for word in keywords:
                key = "%s%s%s" % (word, self.namespace['delimiter'], set)
                if (key in word_count_from_set.keys()) and word_count_from_set[key] > 0:
                    prob = float(word_count_from_set[key]) / float(set_word_counts[set])
                    psets.update({set: prob})

                if psets.get(set) and not math.isinf(float(psets.get(set))) and psets.get(set) > 0:
                    score[set] = psets[set]


        return sorted(score.iteritems(), key=operator.itemgetter(1), reverse=True)[:count]

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
        ret = []
        if isinstance(words, str):
            kws = words.split(" ")
        elif isinstance(words, list):
            kws = words
        else:
            raise Exception('Can only clean String or List.');

        for kw in kws:
            kw = kw.lower()
            kw = sub("[^a-z]", "", kw)

            if kw and len(kw) > self.max_str_len:
                kw = kw.lower()
                if kw:
                    ret.append(kw)

        return ret

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

    def get_set_count(self):
        return self.r.hlen(self.namespace['sets'])

    def get_word_count(self, words):
        return self.r.hmget(self.namespace['words'], words)

    def get_all_words_count(self):
        return self.r.hget(self.namespace['wordcount'], self.namespace['wordcount'])

    def get_set_word_count(self, sets):
        if sets:
            tmp = self.r.hmget(self.namespace['sets'], sets)
            ret = {}
            if tmp:
                i = 0
                for r in tmp:
                    ret[sets[i]] = int(r)
                    i = i + 1

            return ret
        else:
            return 0

    def get_word_count_from_set(self, words, sets):
        if sets:
            keys = []
            for word in words:
                for set in sets:
                    keys.append("%s%s%s" % (word, self.namespace['delimiter'], set))

            tmp = self.r.hmget(self.namespace['words'], keys)
            ret = {}
            if tmp:
                i = 0
                for key in keys:
                    val = tmp[i]
                    if val is None:
                        val = 0
                    else:
                        val = int(val)
                    ret[key] = val
                    i = i + 1
            return ret
        else:
            return {}