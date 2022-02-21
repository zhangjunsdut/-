def ldamodel(num_topics):
    from gensim import corpora, models
    # Global Dictionary
    stopwords = [line.strip() for line in open('D:\\lxw\\第一篇小论文\\论文程序\\LDA主题模型\\中文停用词表.txt', encoding='utf-8').readlines()]  # 加载停用词
    punctuation = [line.strip() for line in open('D:\\lxw\\第一篇小论文\\论文程序\\LDA主题模型\\标点符号.txt', encoding='utf-8').readlines()]#标点符号
    words_nature = ('n', 'nr', 'ns', 'nt', 'eng', 'v', 'd')  # 可用的词性
    def remove_punctuation(ls):  # 去除标点符号
        return [word for word in ls if word not in punctuation]
    def remove_stopwords(ls):  # 去除停用词
        return [word for word in ls if word not in stopwords]
    def remove_word(ls):  # 去除停用词
        return [word for word in ls if len(word) != 1]
    import csv
    import pkuseg
    lexicon = [line.strip() for line in open('D:\\lxw\\第一篇小论文\\论文程序\\LDA主题模型\\自定义词典.txt', encoding='utf-8').readlines()] #希望分词时用户词典中的词固定不分开
    seg = pkuseg.pkuseg(model_name='medicine', user_dict=lexicon)  # 加载模型，给定用户词典
    with open('D:\\lxw\\第一篇小论文\\论文数据\\最终数据.csv', 'r',encoding='gb18030') as csvfile:
        reader = csv.reader(csvfile)
        column6 = [row[5] for row in reader]  # 读取第7列的数据
        words_ls = []
        for text in column6:
            words = remove_word(remove_stopwords(remove_punctuation((seg.cut(text)))))
            words_ls.append(words)
    dictionary = corpora.Dictionary(words_ls)
    corpus = [dictionary.doc2bow(text) for text in
             words_ls]  # corpus里面的存储格式（0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)
    corpora.MmCorpus.serialize('corpus.mm', corpus)
    lda = models.LdaModel(corpus=corpus, id2word=dictionary, random_state=1,
                          num_topics=num_topics)  # random_state 等价于随机种子的random.seed()，使每次产生的主题一致
    topic_list = lda.print_topics(num_topics, 10)
    # print("主题的单词分布为：\n")
    # for topic in topic_list:
    #     print(topic)
    return lda, dictionary
import math
def perplexity(ldamodel, testset, dictionary, size_dictionary, num_topics):
    print('the info of this ldamodel: \n')
    print('num of topics: %s' % num_topics)
    prep = 0.0
    prob_doc_sum = 0.0
    topic_word_list = []
    for topic_id in range(num_topics):
        topic_word = ldamodel.show_topic(topic_id, size_dictionary)
        dic = {}
        for word, probability in topic_word:
            dic[word] = probability
        topic_word_list.append(dic)
    doc_topics_ist = []
    for doc in testset:
        doc_topics_ist.append(ldamodel.get_document_topics(doc, minimum_probability=0))
    testset_word_num = 0
    for i in range(len(testset)):
        prob_doc = 0.0  # the probablity of the doc
        doc = testset[i]
        doc_word_num = 0
        for word_id, num in dict(doc).items():
            prob_word = 0.0
            doc_word_num += num
            word = dictionary[word_id]
            for topic_id in range(num_topics):
                # cal p(w) : p(w) = sumz(p(z)*p(w|z))
                prob_topic = doc_topics_ist[i][topic_id][1]
                prob_topic_word = topic_word_list[topic_id][word]
                prob_word += prob_topic * prob_topic_word
            prob_doc += math.log(prob_word)  # p(d) = sum(log(p(w)))
        prob_doc_sum += prob_doc
        testset_word_num += doc_word_num
    prep = math.exp(-prob_doc_sum / testset_word_num)  # perplexity = exp(-sum(p(d)/sum(Nd))
    print("模型困惑度的值为 : %s" % prep)
    return prep
from gensim import corpora, models
import matplotlib.pyplot as plt
def graph_draw(topic, perplex):  # 做主题数与困惑度的折线图
    x = topic
    y = perplex
    plt.plot(x, y, color="black", linewidth=1)
    plt.xlabel("Number of Topic")
    plt.ylabel("Perplexity")
    plt.show()
if __name__ == '__main__':
    for i in range(5, 6, 1):  # 多少文档中抽取一篇（这里只是为了调试最优结果，可以直接设定不循环）
        print("抽样为" + str(i) + "时的perplexity")
        a = range(1, 20, 5)  # 主题个数20个主题以5为间隔
        p = []
        for num_topics in a:

            lda, dictionary = ldamodel(num_topics)
            corpus = corpora.MmCorpus('corpus.mm')
            testset = []
            for c in range(int(corpus.num_docs / i)):#4篇里面抽取1篇作为测试集，一般20%-30%
                testset.append(corpus[c * i])
            prep = perplexity(lda, testset, dictionary, len(dictionary.keys()), num_topics)
            p.append(prep)

        graph_draw(a, p)