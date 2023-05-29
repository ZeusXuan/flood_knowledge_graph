import re
import os

"""
    example
    value:河北省
    label:LOC
"""
path = "./data"
labelpath =  "./label"
dictpath = "./dict"
flag = False

for dir in sorted(os.listdir(path)):
    dirname = path + "/" + dir
    label_list = []
    # 用于存储每一种label类型的数据
    level1_list = []   
    # 用于保存新闻名
    file_list = []
    # 保存新闻名
    if not flag:
        flag = True
        with open(dictpath + "/" + "新闻名.txt", "w", encoding="utf-8") as f:
            for file in sorted(os.listdir(dirname)):
                f.write(file[5:-4] + "\n")

    for file in sorted(os.listdir(dirname)):
        filename = dirname + "/" + file
        # 用于存储每一则新闻的数据
        level2_list = []
        with open(filename, "r", encoding="utf-8") as f:  # 打开文件
            data = f.read()  # 读取文件
            pattern = " ([^ ()（）,.;'，。、；：“”‘’！？]+?)/([A-Za-z]+) "
            match = re.findall(pattern, data)    
            for value,label in match:
                label_list.append(label)
                level2_list.append((value,label))
        
        # 进行去重
        level1_list.append(list(set(level2_list)))

                
   
    with open(labelpath + "/" + dir + ".txt", "w", encoding="utf-8") as f:
        label_list =list(set(label_list))
        for label in label_list:
            f.write(label + "\n")


    with open(dictpath + "/" + dir + ".txt", "w", encoding="utf-8") as f:
        for level2_list in level1_list:
            for value,label in level2_list:
                f.write(value + " " + label + " ")
            f.write("\n")
    


    


    

                

            
            
                