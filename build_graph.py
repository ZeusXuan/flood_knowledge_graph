from py2neo import Graph,Node
import os

class DisasterGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.dict_path = os.path.join(cur_dir, 'dict')
        self.g = Graph(
            "http://localhost:7474",
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="ilovejiwoo",
            name="neo4j")
        
    '''读取文件'''
    def read_nodes(self):
        # 节点
        news = [] # 新闻名,作为中心节点,有受灾体,受灾数字,开始时间,结束时间四个属性
        days = [] # 日期        
        locs = [] # 发生位置

        # 构建节点实体关系
        news_begin_days = [] # 新闻开始日期
        news_end_days = [] # 新闻结束日期
        news_locs = [] # 新闻名发生位置

        count = 0
        news_db = [] # 用于存储新闻名对应的受灾体
        news_number = []
        news_time = [] # 用于存储新闻时间

        # 读入新闻名
        with open(self.dict_path + "/" + "新闻名.txt", 'r', encoding="utf-8") as f:
            for line in f:
                count += 1
                line = line.strip()  # 去除每行末尾的换行符
                # 处理每行数据
                news.append(line)
                print(count)

        # 读入新闻对应的受灾实体
        with open(self.dict_path + "/" + "承载体标签.txt", 'r', encoding="utf-8") as f:
            for line in f:
                line = line.strip()  # 去除每行末尾的换行符
                db_list = line.split(" ")
                temp_list = []
                for i in range(len(db_list)):
                    if db_list[i] == "DB":
                        temp_list.append(db_list[i-1])
                news_db.append(set(list(temp_list)))


        # 读入新闻对应的受灾数据
        with open(self.dict_path + "/" + "人口面积等标签.txt", 'r',encoding = "utf-8") as f:
            for line in f:
                line = line.strip()  # 去除每行末尾的换行符
                number_list = line.split(" ")
                temp_dict = dict()
                for i in range(len(number_list)):
                    if number_list[i] == "AImp":
                        temp_dict["受灾人数"] = number_list[i-1]
                    elif number_list[i] == "AInp":
                        temp_dict["受伤人数"] = number_list[i-1]
                    elif number_list[i] == "ADP":
                        temp_dict["死亡人数"] = number_list[i-1]
                    elif number_list[i] == "AWD":
                        temp_dict["积水深度"] = number_list[i-1]
                    elif number_list[i] == "AMP":
                        temp_dict["失踪人数"] = number_list[i-1]
                    elif number_list[i] == "AIAC":
                        temp_dict["受灾面积"] = number_list[i-1]
                    elif number_list[i] == "ATP":
                        temp_dict["转移人数"] = number_list[i-1]      
                    elif number_list[i] == "AE":
                        temp_dict["经济损失"] = number_list[i-1]
                    elif number_list[i] == "ATAC":
                        temp_dict["绝收面积"] = number_list[i-1]
                    elif number_list[i] == "ASAC":
                        temp_dict["成灾面积"] = number_list[i-1]
                    elif number_list[i] == "ATC":
                        temp_dict["倒塌房屋"] = number_list[i-1]

                news_number.append(temp_dict)


        # 读入新闻对应的时间
        with open(self.dict_path + "/" + "时间标签.txt", 'r',encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                time_list = line.split(" ")
                temp_time_dict = dict()
                temp_begin_day = []
                temp_end_day = []
                for i in range(len(time_list)):
                    if time_list[i] == "DS":
                        temp_begin_day.append(time_list[i-1])
                    elif time_list[i] == "DO":
                        temp_end_day.append(time_list[i-1])
                    elif time_list[i] == "TS":
                        temp_time_dict["开始时间"] = time_list[i-1]
                    elif time_list[i] == "TO":
                        temp_time_dict["结束时间"] = time_list[i-1]

                days += temp_begin_day
                days += temp_end_day
                news_begin_days.append(list(set(temp_begin_day)))
                news_end_days.append(list(set(temp_end_day)))
                news_time.append(temp_time_dict)
                                        
        # 读入新闻对应的地点
        with open(self.dict_path + "/" + "暴雨洪涝位置.txt", 'r',encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                loc_list = line.split(" ")
                temp_list = []
                for i in range(len(loc_list)):
                    if i%2 == 0:
                        temp_list.append(loc_list[i])
                news_locs.append(list(set(temp_list))) 
                locs += temp_list
                        
        return news,set(days),set(locs),\
            news_begin_days,news_end_days,news_locs,\
            news_db,news_number,news_time
    
    '''建立节点'''
    def create_node(self, label, nodes):
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
        return
    

    '''创建新闻节点'''
    def create_news_node(self, news, news_db, news_number, news_time):
        for i in range(len(news)):
            """
            用于存储新闻名对应的受灾数量,每一项为一个字典
            AImp 受灾人数
            AInp 受伤人数
            ADP 死亡人数
            AWD 积水深度
            AMP 失踪人数
            AIAC 受灾面积
            ATP 转移人数
            AE 经济损失
            ATAC 绝收面积
            ASAC 成灾面积
            AHC 倒塌房屋
            """
            node = Node("新闻", name = news[i],sufferings = ','.join(news_db[i]),
                        begintime = news_time[i].get("开始时间","无"),endtime = news_time[i].get("结束时间","无"),
                        aimp = news_number[i].get("受灾人数","无"), ainp = news_number[i].get("受伤人数","无"),
                        adp = news_number[i].get("死亡人数","无"),awd = news_number[i].get("积水深度","无"),
                        amp = news_number[i].get("失踪人数","无"),aiac = news_number[i].get("受灾面积","无"),
                        atp = news_number[i].get("转移人数","无"),ae = news_number[i].get("经济损失","无"),
                        atac = news_number[i].get("绝收面积","无"), asac = news_number[i].get("成灾面积","无"),
                        ahc = news_number[i].get("倒塌房屋","无"))
            self.g.create(node)
        
        return

    '''创建知识图谱所有实体节点'''
    def create_graphnodes(self):
        news,days,locs,news_begin_days,news_end_days,news_locs,news_db,news_number,news_time = self.read_nodes()
        self.create_news_node(news,news_db,news_number,news_time)
        self.create_node("日期", days)
        self.create_node("地点", locs)
        return


    '''创建所用实体关系边'''
    def create_graphrels(self):
        news,days,locs,news_begin_days,news_end_days,news_locs,news_db,news_number,news_time = self.read_nodes()
        self.create_relationship("新闻","日期",news_end_days, "news_end_days", "结束日期" ,news)
        self.create_relationship("新闻","日期",news_begin_days, "news_begin_days", "开始日期",news)
        self.create_relationship("新闻","地点",news_locs, "news_locs", "发生地点" ,news)
        return
    
    '''创建实体关系边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name, news):
        count = 0
        for i in range(len(news)):
            p = news[i]
            for q in edges[i]:
                query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
                # 打印相应的信息
                try:
                    self.g.run(query)
                    count += 1
                    print(rel_type, count)
                except Exception as e:
                    print(e)

        return


if __name__ == '__main__':
    handler = DisasterGraph()
    print("step1:导入图谱节点中")
    handler.create_graphnodes()
    print("step2:导入图谱边中")      
    handler.create_graphrels()
