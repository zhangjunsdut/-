import networkx as nx
import pandas as pd
import numpy as np
import csv
import re
g = nx.DiGraph()
node_filename = "D:\\lxw\\第一篇小论文\\关键用户识别\\node.csv"
edge_filename = "D:\\lxw\\第一篇小论文\\关键用户识别\\edge.csv"
csv_node=open(node_filename)
csv_edge=open(edge_filename)
node_line = csv_node.readline()  # 逐行读取点文件
while node_line:
    temp_line = re.split(',', node_line)
    # print(temp_line)
    g.add_node(temp_line[0])
    node_line = csv_node.readline()

print('node_num',g.number_of_nodes())
print(g.nodes)
print(type(g.nodes))
edge_line = csv_edge.readline()  # 逐行读取边文件
while edge_line:
    temp_line = re.split(",", edge_line)  # 把边文件中的每一行用","分隔开
    temp_line[1] = temp_line[1].replace('\n', '').replace('\r', '')  # 去除文本内容中的换行符
    # print(temp_line)
    g.add_edge(temp_line[0], temp_line[1])  # 向网络中添加边
    edge_line = csv_edge.readline()

print('edge_num',g.number_of_edges())
step =0
results = []
node_score =pd.read_excel(r'D:\\lxw\\第一篇小论文\\关键用户识别\\节点排序.xlsx') #默认读取第一个sheet,sheet_name=2
print(node_score['node_Id4'])
for i in node_score['node_Id4']:
    i=str(i)
    print('i',i)
    g.remove_node(i)
    print('step',step)
    N = g.number_of_nodes()
    print('N',N)
    print('edge_num',g.number_of_edges())
    sumeff =0
    for u in g.nodes():  # 遍历流量图F的每个点
        path = nx.shortest_path_length(g,source=u)  # 在网络G中计算从u开始到其他所有节点（注意包含自身）的最短路径长度。如果两个点之间没有路径，那path里也不会存储这个目标节点（比前面的代码又省了判断是否has_path的过程）
        for v in path.keys():  # path是一个字典，里面存了所有目的地节点到u的最短路径长度
            if u != v:  # 如果起终点不同才累加计算效率
                sumeff += 1 / path[v]
    result = (1 / (N * (N - 1))) * sumeff  # 计算网络剩余效率
    print('result',result)
    results.append(result)
    step = step + 1
    if result == 0:
        break
print('results',results)
f = open('C:\\Users\\Administrator\\Desktop\\网络效率.csv', 'w', encoding='gb18030', newline='')
csv_writer = csv.writer(f)
for i in results:
    i=list(i)
    csv_writer.writerow(i)
print('处理完成')

#     g = nx.DiGraph()
#     node_filename = "D:/lxw/第一篇小论文/关键用户识别/node.csv"
#     edge_filename = "D:/lxw/第一篇小论文/关键用户识别/edge.csv"
#     csv_node = open(node_filename)
#     csv_edge = open(edge_filename)
#     node_line = csv_node.readline()  # 逐行读取点文件
#     while node_line:
#         temp_line = re.split(',', node_line)
#         # print(temp_line)
#         g.add_node(temp_line[0])
#         node_line = csv_node.readline()
#
#     print('node_num', g.number_of_nodes())
#     print(g.nodes)
#     print(type(g.nodes))
#     edge_line = csv_edge.readline()  # 逐行读取边文件
#     while edge_line:
#         temp_line = re.split(",", edge_line)  # 把边文件中的每一行用","分隔开
#         temp_line[1] = temp_line[1].replace('\n', '').replace('\r', '')  # 去除文本内容中的换行符
#         # print(temp_line)
#         g.add_edge(temp_line[0], temp_line[1])  # 向网络中添加边
#         edge_line = csv_edge.readline()
#
#     print('edge_num', g.number_of_edges())

# g.remove_node('1307')
# N = g.number_of_nodes()
# print('N',N)
# print('edge_num',g.number_of_edges())
# sumeff =0
# for u in g.nodes():  # 遍历流量图F的每个点
#     path = nx.shortest_path_length(g,source=u)  # 在网络G中计算从u开始到其他所有节点（注意包含自身）的最短路径长度。如果两个点之间没有路径，那path里也不会存储这个目标节点（比前面的代码又省了判断是否has_path的过程）
#     for v in path.keys():  # path是一个字典，里面存了所有目的地节点到u的最短路径长度
#         if u != v:  # 如果起终点不同才累加计算效率
#             sumeff += 1 / path[v]
# result = (1 / (N * (N - 1))) * sumeff  # 计算网络剩余效率
# print('result',result)