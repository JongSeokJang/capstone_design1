import networkx
import re
import os
import math
#from konlpy.tag import Mecab
from konlpy.tag import Komoran
cwd = os.path.dirname(os.path.realpath(__file__))

def repl(m):
    return ' ' * len(m.group())
# keywords, sentences
class TextRank:


    # quote remover and line splitter  result convert
    def convert_to_original_string(self, strings, original):
        idx = 0
        res = []
        for string in strings:
            new_string = ""
            for i in range((len(string))):
                new_string += original[idx]
                idx += 1
            res.append(new_string)
        return res

    # split content to list of sentences
    def readSentence(self):

        # split content using regular expression
        content = re.sub(self.quoteRemover, repl, self.content)
        ch = self.lineSplitter.split(content)
        ch = self.convert_to_original_string(ch, self.content)

        # concatenate sentence and delimiter
        for s in map(lambda a, b: a+b, ch[::2], ch[1::2]):
            if not s: continue

            # remove left/right space
            yield s.strip()

    # split content to list of keywords
    def readTagger(self):
        # split content using regular expression
        content = re.sub(self.quoteRemover, repl, self.content)
        ch = self.lineSplitter.split(content)
        ch = self.convert_to_original_string(ch, self.content)

        # concatenate sentence and delimiter
        for s in map(lambda a, b: a+b, ch[::2], ch[1::2]):
            if not s: continue

            # pos tagger apply
            try:
                yield self.tagger.pos(s)
            except:
                []

    def readTaggerForTitle(self):
        return self.tagger.pos(self.title)

    # build additional graph information for applying pagerank algorithm
    def loadTagger(self):
        # construct bigram count dictionary
        def insertPair(a, b):
            if a > b:
                a, b = b, a
            elif a == b:
                return
            self.taggerDictBiCount[a, b] = self.taggerDictBiCount.get((a, b), 0) + 1

        def insertNearPair(a, b):
            self.dictNear[a, b] = self.dictNear.get((a, b), 0) + 1

        taggerIter = self.readTagger()
        wordFilter = self.taggerTokenizer

        for sent in taggerIter:
            sent = list(filter(self.englishFilter, sent))
            for i, word in enumerate(sent):

                # english filtering

                # filtering
                if wordFilter and not wordFilter(word):
                    continue

                self.taggerDictCount[word] = self.taggerDictCount.get(word, 0) + 1
                self.nTotal += 1

                # create bigram for similar word filtering
                joined1 = '%s %s' % (sent[i-1][0], word[0])
                joined2 = '%s%s' % (sent[i-1][0], word[0])
                # news content based bigram
                joined3 = '%s %s' % (word[0], sent[i+1][0])
                joined4 = '%s%s' % (word[0], sent[i+1][0])
                # check similar word (ex: iPhone6, iPhone 6)
                # inset near pair. then, similar word is removed
                if i - 1 >= 0 and wordFilter(sent[i-1]) and (wordFilter((joined1, 'NNG')) or wordFilter((joined2, 'NNG'))):
                    insertNearPair(sent[i-1], word)
                if i + 1 < len(sent) and wordFilter(sent[i+1]) and (wordFilter((joined3, 'NNG')) or wordFilter((joined4, 'NNG'))):
                    insertNearPair(word, sent[i+1])

                # construct bigram count
                for j in range(i+1, min(i + self.window + 1, len(sent))):
                        if wordFilter and not wordFilter(sent[j]):
                            continue
                        joined1 = '%s %s' % (word[0], sent[j][0])
                        joined2 = '%s%s' % (word[0], sent[j][0])
                        if sent[j] != word and (wordFilter((joined1, 'NNG')) or wordFilter((joined2, 'NNG'))):
                            insertPair(word, sent[j])

        # similar word count concatenate (ex: iPhone6, iPhone 6)
        unigrams = self.taggerDictCount.keys()
        for key in self.taggerDictBiCount.keys():
            joined1 = ('%s%s' % (key[0][0], key[1][0]), 'NNG')
            joined2 = ('%s%s' % (key[0][0], key[1][0]), 'NNP')
            if joined1 in unigrams:
                self.taggerDictCount[joined1] = self.taggerDictCount.get(joined1, 0) + self.taggerDictBiCount.get(key, 0)
                self.taggerDictBiCount[key] = 0
            if joined2 in unigrams:
                self.taggerDictCount[joined1] = self.taggerDictCount.get(joined2, 0) + self.taggerDictBiCount.get(key, 0)
                self.taggerDictBiCount[key] = 0


    # build additional graph information for applying pagerank algorithm
    def loadSentence(self):
        # get similarity of two sentences
        def similarity(a, b):
            n = len(a.intersection(b))
            return n / float(len(a) + len(b) - n) / (math.log(len(a) + 1) * math.log(len(b) + 1))

        sentSet = []
        sentenceIter = self.readSentence()
        for sent in filter(None, sentenceIter):
            if type(sent) == str:
                s = set(filter(None, self.sentenceTokenizer(sent)))
            if len(s) < 2:
                continue
            self.sentenceDictCount[len(self.sentenceDictCount)] = sent
            sentSet.append(s)

        for i in range(len(self.sentenceDictCount)):
            for j in range(i+1, len(self.sentenceDictCount)):
                s = similarity(sentSet[i], sentSet[j])
                if s < self.threshold:
                    continue
                self.sentenceDictBiCount[i, j] = s

    # build keyword graph
    def loadKeywordGraph(self):
        self.taggerGraph = networkx.Graph()
        self.taggerGraph.add_nodes_from(self.taggerDictCount.keys())

        unigrams = self.taggerDictCount.keys()
        wordFilter = self.taggerTokenizer
        for (a, b), n in self.taggerDictBiCount.items():
            self.taggerGraph.add_edge(a, b, weight=n*n*n*self.coef + (1 - self.coef))

    # build sentence graph
    def loadSentenceGraph(self):
        self.sentenceGraph = networkx.Graph()
        self.sentenceGraph.add_nodes_from(self.sentenceDictCount.keys())

        for (a, b), n in self.sentenceDictBiCount.items():
            self.sentenceGraph.add_edge(a, b, weight=n*n*n*self.coef + (1 - self.coef))

    # pagerank
    def pagerank(self, graph):
        return networkx.pagerank(graph, weight='weight')

    # get Information I(X) = -log(p, X)
    def getI(self, a):
        if a not in self.taggerDictCount:
            return None
        else:
            return math.log(self.nTotal / self.taggerDictCount[a])

    # get Pointwise Mutual Information PMI(X, Y) = log(P(X intersection Y) / (P(X) * P(y)))
    def getPMI(self, a, b):
        co = self.dictNear.get((a, b), 0)
        if not co:
            return None
        else:
            return math.log(float(co) * self.nTotal / self.taggerDictCount[a] /
                    self.taggerDictCount[b])

    # pagerank apply
    def keyword_rank(self):
        self.loadTagger()
        self.loadKeywordGraph()
        self.keyword_ranks = self.pagerank(self.taggerGraph)

    # get keywords
    def keywords(self, num=15):
        ranks = self.keyword_ranks
        wordFilter = self.taggerTokenizer
        cand = sorted(ranks, key=ranks.get, reverse=True)
        pairness = { }
        startOf = { }
        tuples = { }
        for k in cand:
            if k[1] != 'VA' and k[1] != 'VV':
                tuples[(k, )] = self.getI(k) * ranks[k]
            for l in cand:
                if k == l:
                    continue
                pmi = self.getPMI(k, l)
                if pmi:
                    pairness[k, l] = pmi

        for (k, l) in sorted(pairness, key=pairness.get, reverse=True):
            if k not in startOf:
                startOf[k] = (k, l)

        for (k, l), v in pairness.items():
            pmis = v
            rs = ranks[k] * ranks[l]
            path = (k, l)
            tuples[path] = pmis / (len(path) - 1) * rs ** (1 / len(path)) * len(path)
            last = l
            while last in startOf and len(path) < 7:
                if last in path:
                    break
                pmis += pairness[startOf[last]]
                last = startOf[last][1]
                rs *= ranks[last]
                path += (last, )
                # G(TR) * A(PMI) * Length
                tuples[path] = pmis / (len(path) - 1) * res ** (1 / len(path)) * len(path)

        used = set()
        both = { }
        for k in sorted(tuples, key=tuples.get, reverse=True):
            if used.intersection(set(k)):
                continue
            both[k] = tuples[k]
            for w in k:
                used.add(w)

        res = []

        avg = 0.0
        for key in both.keys():
            avg += both[key]
        if len(both.keys()) > 0:
            avg /= len(both.keys())

        titleWords = list(filter(wordFilter, self.readTaggerForTitle()))
        titleWords = list(map(lambda x: x[0], titleWords))
        for key in both.keys():
            if len(key) == 2:
                if self.taggerDictCount[key[0]] <= self.minimum_low_freq or self.taggerDictCount[key[1]] <= self.minimum_low_freq:
                    both[key] -= avg * self.low_freq_word_subtraction_multiplier
                if key[0][0] in titleWords or key[1][0] in titleWords:
                    both[key] += avg * self.title_word_addition_multiplier
                joined1 = '%s %s' % (key[0][0], key[1][0])
                joined2 = '%s%s' % (key[0][0], key[1][0])
                if joined1 in self.content and wordFilter((joined1, 'NNG')):
                    res.append((joined1, both[key]))
                elif joined2 in self.content and wordFilter((joined2, 'NNG')):
                    res.append((joined2, both[key]))
            else:
                if self.taggerDictCount[key[0]] <= self.minimum_low_freq:
                    both[key] -= avg * self.low_freq_word_subtraction_multiplier
                if key[0][0] in titleWords:
                    both[key] += avg * self.title_word_addition_multiplier

                # 수사가 아니면 단일 단어 추가
                if key[0][1] != 'SN':
                    res.append(('%s' % (key[0][0]), both[key]))

        res = list(filter(lambda x: x[1] > 0.0, res))
        return sorted(res, key=lambda x: x[1], reverse=True)[:num]

    # pagerank apply
    def sentence_rank(self):
        self.loadSentence()
        self.loadSentenceGraph()
        self.sentence_ranks = self.pagerank(self.sentenceGraph)

    # get sentences
    def sentences(self, ratio = 0.333):

        r = self.sentence_ranks
        ks = sorted(r, key=r.get, reverse=True)[:int(len(r)*ratio)]

        ks = list(map(lambda k:(self.sentenceDictCount[k], r[k]), sorted(ks)))
        return sorted(ks, key=lambda x: x[1], reverse=True)

    def __init__(self, **kwargs):

        self.graph = None
        #self.tagger = Mecab()
        self.tagger = Komoran()
        #Switch this to Mecab in server
        self.window = kwargs.get('window', 5)
        self.coef = kwargs.get('coef', 1.0)
        self.threshold = kwargs.get('threshold', 0.005)
        self.content = kwargs.get('content', '')
        self.title = kwargs.get('title', '')
        self.stopwords = kwargs.get('stopwords', set([]))
        self.singlewords = kwargs.get('singlewords', set([]))
        self.english = kwargs.get('english', set([]))
        self.title_word_addition_multiplier = kwargs.get('title_word_addition_multiplier', 1)
        self.minimum_low_freq = kwargs.get('minimum_low_freq', 1)
        self.low_freq_word_subtraction_multiplier = kwargs.get('low_freq_word_subtraction_multiplier', 0)
        self.keyword_ranks = []
        self.sentence_ranks = []

        # line splitter
        self.quoteRemover = '"[^"]*"|\'[^\']*\'|\([^()]*\)|\{[^{}]*\}|\[[^\[\]]*\]|\<[^\<\>]*\>|`[^`]*`'
        self.lineSplitter = re.compile('(다[.!?:](?=[^"\'\`\]\}\)\.\!\?]))')

        # variables for keyword extract
        self.taggerDictCount = { }
        self.taggerDictBiCount = { }
        self.dictNear = { }
        self.nTotal = 0

        # only extract keyword NNG, NNP (일반 명사, 고유 명사, 외국어, 숫자, 한자 제외), 영어일 경우 영어 명사 사전에 등록된 단어인지 검색
        self.taggerTokenizer = lambda x: x[0] not in self.stopwords and x[1] in ('NNG', 'NNP', 'SL', 'SN') and (len(x[0]) > 1 or x[0] in self.singlewords) and re.compile('[一-龥]+').match(x[0]) is None

        self.englishFilter = lambda x: x[1] != 'SL' or x[0].lower() in self.english

        # variables for sentence summarization
        self.sentenceDictCount = { }
        self.sentenceDictBiCount = { }
        self.sentenceTokenizer = lambda sent: filter(lambda x : x[0] not in self.stopwords and x[1] in ('NNG', 'NNP', 'VV', 'VA', 'SL', 'SN'), self.tagger.pos(sent))
