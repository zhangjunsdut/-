from gensim import corpora, models
import pandas as pd
# Global Dictionary
stopwords = [line.strip() for line in open('D:\\lxw\\第一篇小论文\\论文程序\\LDA主题模型\\中文停用词表.txt', encoding='utf-8').readlines()]#加载停用词
punctuation = [line.strip() for line in open('D:\\lxw\\第一篇小论文\\论文程序\\LDA主题模型\\标点符号.txt', encoding='utf-8').readlines()]#标点符号
words_nature = ('n', 'nr', 'ns', 'nt', 'eng', 'v', 'd')  # 可用的词性
def remove_punctuation(ls):  # 去除标点符号
    return [word for word in ls if word not in punctuation]
def remove_stopwords(ls):  # 去除停用词
    return [word for word in ls if word not in stopwords]
def remove_word(ls):  # 去除停用词
        return [word for word in ls if len(word) != 1]
import pkuseg
import csv
lexicon = [line.strip() for line in open('D:\\lxw\\第一篇小论文\\论文程序\\LDA主题模型\\自定义词典.txt', encoding='utf-8').readlines()] #希望分词时用户词典中的词固定不分开
seg = pkuseg.pkuseg(model_name='medicine',user_dict=lexicon)  #加载模型，给定用户词典
with open('D:\\lxw\\第三篇小论文\\最终数据.csv','r',encoding='gb18030') as csvfile:
    reader = csv.reader(csvfile)
    column6 = [row[5] for row in csvfile]#读取第6列的数据
    words_ls = []
    for text in column6:
        print('text',text)
        words = remove_word(remove_stopwords(remove_punctuation((seg.cut(text)))))  # 进行分词
        print(words)
        words_ls.append(words)
print("words_ls",words_ls)
# data = pd.read_csv(r'D:\\lxw\\第三篇小论文\\最终数据.csv',header=None,encoding='gb18030')
# # import csv
# # f = open('D:\\lxw\\最终数据.csv', 'w', encoding='gb18030', newline='')
# # csv_writer = csv.writer(f)
# # # 3. 构建列表头
# # csv_writer.writerow(["keywords"])
# words_ls = []
# for i in data[5]:
#     i = str(i)
#     # print('i',i)
#     word = []
#     words = remove_word(remove_stopwords(remove_punctuation((seg.cut(i)))))  # 进行分词
#     print(words)
#     words_ls.append(words)
#     for j in words:
#         if j not in word:
#             word.append(j)
#     # c = len (word)
#     # print(c)
#     # csv_writer.writerow([c] + [word])
print('处理完成')
# 生成语料词典
dictionary = corpora.Dictionary(words_ls)
print(dictionary)
# 生成稀疏向量集
corpus = [dictionary.doc2bow(words) for words in words_ls]
# LDA模型，num_topics设置聚类数，即最终主题的数量
lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=6)
# print(lda)
# 展示每个主题的前20的词语
for topic in lda.print_topics(num_words=20):
    print(topic)
# for i in range(6):
#     a = len(lda.print_topic(i))
#     print('len',a)
# # 推断每个语料库中的主题类别
print('推断：')
for e, values in enumerate(lda.inference(corpus)[0]):
    topic_val = 0
    topic_id = 0
    for tid, val in enumerate(values):
        if val > topic_val:
            topic_val = val
            topic_id = tid
    print(topic_id, '->', column6[e])
import pandas as pd
data = pd.DataFrame(lda.print_topics())
data.to_csv('D:\\lxw\\主题.txt', sep='\t', index=0, header=0)
print('推断：')
# 1. 创建文件对象
f = open('D:\\lxw\\主题.csv','w',encoding='utf-8',newline='')
# 2. 基于文件对象构建 csv写入对象
csv_writer = csv.writer(f)
# 3. 构建列表头
csv_writer.writerow(["id"])
for e, values in enumerate(lda.inference(corpus)[0]):
    topic_val = 0
    topic_id = 0
    for tid, val in enumerate(values):
        if val > topic_val:
            topic_val = val
            topic_id = tid
    print(topic_id)
    print(type(topic_id))
    # 4. 写入csv文件内容
    csv_writer.writerow([topic_id])
f.close()
print('处理完成')