import random

import numpy as np

#该文件为数据集构造函数 根据用户个数，服务器个数，docker类型以及最大购买数d进行数据集的构造
def generate_dataset(num_users, num_servers, num_docker_types,d):
    R = [] # R为用户连接约束矩阵 R[i][j] 就代表用户i对云服务器j是否可连接 1为可连接 0为不可连接 不能连接就不能在上面购买docker
    for _ in range(num_users):
        ones = random.sample(range(num_servers), random.randint(1, num_servers))
        R.append([1 if i in ones else 0 for i in range(num_servers)])

    B = np.zeros((num_users, num_docker_types))  # 初始化B矩阵为全0  该矩阵为用户对想要docker的报价矩阵 B[i][k] 为用户i对第k种docker的报价
    I = np.zeros((num_users, num_docker_types))  # 初始化I矩阵为全0  该矩阵为用户对想要docker的数字矩阵 I[i][k] 为用户i是否想要第k种docker
                                                    # 1为想要 0为不要
    for i in range(num_users):
        positions = random.sample(range(num_docker_types), random.randint(1, num_docker_types))
        for pos in positions:
            B[i][pos] = random.gauss(50, 15) #用户报价为标准值为50 方差为15的高斯分布 精确到小数点后一位
            B[i][pos] = round(B[i][pos], 1)
        #num_to_select = random.randint(1, len(positions))
        #selected_positions = random.sample(positions, num_to_select)
        # 将选中的位置在 I[i] 中赋值为 1
        #if len(selected_positions) < d:
           # lenth = len(selected_positions)
        #else:
            #lenth = d
        #for k in range(lenth):
                #pos = selected_positions[k]
                #I[i][pos] = 1

    # Q矩阵为库存矩阵 Q[j][k]就代表 云服务器j 的第k种docker所剩库存为多少
    Q = [[3 for _ in range(num_docker_types)] for _ in range(num_servers)]

    return Q, R, B

def get_dataset(dataset, num_users_to_extract,d):
    Q, R, B = dataset
    I = np.zeros((len(B), len(B[0])))
    indices = random.sample(range(len(B)), num_users_to_extract)
    for i in indices:
        positions = []
        for k in range(len(B[0])):
          if B[i][k] != 0:
              positions.append(k)
        selected_positions = random.sample(positions, random.randint(1, len(positions)))
        if len(selected_positions) < d:
            lenth = len(selected_positions)
        else:
            lenth = d
        for k in range(lenth):
                pos = selected_positions[k]
                I[i][pos] = 1
    extracted_I = [I[i] for i in indices]
    extracted_R = [R[i] for i in indices]
    extracted_B = [B[i] for i in indices]

    return Q, extracted_R, extracted_B, extracted_I
