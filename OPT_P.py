import numpy as np
from docplex.mp.model import Model


def opt_p(Q, R, B, p, d):
    num_users = len(B)
    num_servers = len(Q)
    num_docker_types = len(Q[0])
    initial_prices = np.zeros((num_servers, num_docker_types))

    # 创建模型
    model = Model()
    # 定义决策变量
    x = [[[model.binary_var(name=f"x_{i}_{j}_{k}") for k in range(num_docker_types)] for j in range(num_servers)] for i
         in range(num_users)]
    y = [model.integer_var(lb=1, ub=num_users, name=f"y_{i}") for i in range(num_users)]
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
        model.add(model.sum(x[i][j][k] * R[i][j] for j in range(num_servers) for k in range(num_docker_types)) <= d)
    # 每个用户最多分配一个Docker类型约束
    for i in range(num_users):
        for k in range(num_docker_types):
            model.add(model.sum(x[i][j][k] * R[i][j] for j in range(num_servers)) <= 1)
    for i in range(num_users):
        for j in range(num_servers):
            for k in range(num_docker_types):
                model.add(x[i][j][k] * R[i][j] * p[j][k] <= x[i][j][k] * R[i][j] * B[i][k])

    # for j in range(num_servers):
    # for k in range(num_docker_types):
    # model.add(model.sum(x[i][j][k] * B[i][j] for i in range(num_users)) >= model.sum(initial_prices[j][k] * x[i][j][k] for i in range(num_users)))
    # 最优顺序

    # 求解模型
    solution = model.solve()
    x1 = [[[x[i][j][k].solution_value for k in range(num_docker_types)] for j in range(num_servers)] for i in
          range(num_users)]

    # 输出结果
    if solution:
        print("Best Objective Balue:", model.objective_value)
        print("Best Assignment of Docker to Users:")
        for i in range(num_users):
            for j in range(num_servers):
                for k in range(num_docker_types):
                    if x[i][j][k].solution_value > 0:
                        print(f"User {i}, Server {j}, Docker {k}: {x[i][j][k].solution_value}")
        print("User Arrival Order:")
        user_order = sorted(range(num_users), key=lambda i: y[i].solution_value)
        # 最优顺序
        print(user_order)
        prices = initial_prices.copy()
        print("Initial Prices:")
        print(initial_prices)

        return p, x1

R = [[0, 1], [1,  0], [1, 1]]  # 用户i对于服务器 j 是否可以连接（部署约束）用Rij 表示，Rij =1表示可以连接。
B = [[7, 3], [4, 4], [3, 8]]  # 用户 i 对 k 类型 docker 的估值可以用vik 表示
Q = [[1, 1], [1, 1]]  # 每个 EQS 拥有的 docker 个数
d = 2
p = [[2,2],[3.5,4]]
x=opt_p(Q, R, B, p,d)
print(x)