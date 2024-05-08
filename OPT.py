import numpy as np
from docplex.cp.model import *
from docplex.mp.model import Model


def opt(Q, R, B, d):
    num_users = len(B)  # 用户个数
    num_servers = len(Q)  # 云服务器个数
    num_docker_types = len(Q[0])  # docker种类个数

    # 创建模型
    model = Model()
    # 定义决策变量
    x = [[[model.binary_var(name=f"x_{i}_{j}_{k}") for k in range(num_docker_types)] for j in range(num_servers)]
         for i in range(num_users)]
    # 目标函数
    model.maximize(model.sum(
        B[i][k] * x[i][j][k] * R[i][j] for i in range(num_users) for j in range(num_servers) for k in
        range(num_docker_types)))
    # 约束条件
    # Docker数量约束
    for j in range(num_servers):
        for k in range(num_docker_types):
            model.add(model.sum(x[i][j][k] * R[i][j] for i in range(num_users)) <= Q[j][k])
    # 用户Docker数量约束
    for i in range(num_users):
        model.add(
            model.sum(x[i][j][k] * R[i][j] for j in range(num_servers) for k in range(num_docker_types)) <= d)
    # 每个用户最多分配一个Docker类型约束
    for i in range(num_users):
        for k in range(num_docker_types):
            model.add(model.sum(x[i][j][k] * R[i][j] for j in range(num_servers)) <= 1)

    # 求解模型
    solution = model.solve()
    x1 = [[[x[i][j][k].solution_value for k in range(num_docker_types)] for j in range(num_servers)] for i in
          range(num_users)]

    # 输出结果
    if solution:
       return x1
R = [[0, 1], [1,  0], [1, 1]]  # 用户i对于服务器 j 是否可以连接（部署约束）用Rij 表示，Rij =1表示可以连接。
B = [[7, 3], [4, 4], [3, 8]]  # 用户 i 对 k 类型 docker 的估值可以用vik 表示
Q = [[1, 1], [1, 1]]  # 每个 EQS 拥有的 docker 个数
d = 2
x = opt(Q,R,B,d)
print(x)
