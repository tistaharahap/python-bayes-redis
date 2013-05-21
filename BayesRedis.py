import redis, math

class BayesRedis():
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

    def __init__(self):
        self.r = redis.StrictRedis(host=self.reds['host'], port=self.reds['port'], db=self.reds['db'])
        if self.r is None:
            raise Exception('Redis is not properly setup. Check redis configs?')

        # Namespacing
        for key in self.namespace:
            if key not in ['global', 'delimiter', 'wordcount']:
                self.namespace[key] = '%s-%s' % (self.namespace['global'], self.namespace[key])

    def classify(self, words, count=10, offset=0):
        score = []

        keywords = self.clean_keywords(words)
        sets = self.get_all_sets()
        P = {
            'sets': {}
        }

        set_word_counts = self.get_set_word_count(sets)
        word_count_from_set = self.get_word_count_from_set(words, sets)

        for set in sets:
            for word in words:
                key = "%s%s%s" % (word, self.namespace['delimiter'], set)
                if word_count_from_set[key]:
                    if word_count_from_set[key] > 0:
                        P.sets[set] = P.sets[set] + (word_count_from_set[key] / set_word_counts[set])

                if not math.isinf(P.sets[set]) and P.sets[set] > 0:
                    score[set] = P.sets[set]

        score = sorted(score)
        print score
        return score

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
            #kw.sub("/[^a-z]/i", "", kw)

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
        return self.r.hmget(self.namespace['sets'], sets)

    def get_word_count_from_set(self, words, sets):
        keys = []
        for word in words:
            for set in sets:
                keys.append("%s%s%s" % (word, self.namespace['delimiter'], set))

        return self.r.hmget(self.namespace['words'], keys)

bayes = BayesRedis()
bayes.classify("Batista adalah laki-laki")