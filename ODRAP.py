import random
import numpy as np
from data import generate_dataset


# 该算法为在线定价以及分配算法 通过同一时间进入不同数量的用户，对其分配情况进行二分支付计算，求得定价。
# 为了确保得知用户想要的docker  我们引入了集合I[i][k] 如果I[i][k] = 1，则代表该用户i想要第k种docker
def odrap(Q, R, B, I, user_order, d):
    def payment(Q, R, B, I, order, P, X, d):
        for i in order:
            if X[i] == 1:
                B1 = np.copy(B)
                left, right = 0, B1[i]
                B1[i] = (left + right) / 2
                while abs(left - right) >= 0.000001:
                    Q1 = np.copy(Q)
                    X1 = np.zeros(len(B))
                    allocation1, _ = allocation(Q1, R, B1, I, order, P, X1, d)
                    if allocation1[i] != 0:
                        right = B1[i]
                        B1[i] = (left + right) / 2
                    else:
                        left = B1[i]
                        B1[i] = (left + right) / 2

                P[i] = (left + right) / 2

        return P

    def allocation(Q, R, B, I, order, P, X, d):
        densities = []

        total_inventory = 0
        for i in order:
            density = B[i] / np.sqrt(d)
            densities.append(density)

        user_indices = sorted(range(len(order)), key=lambda i: densities[i], reverse=True)

        for i in user_indices:
            x = -1
            y = -1

            storage_list = []
            for k in range(len(Q[0])):
                for j in range(len(Q)):
                    if (Q[j][k] > 0 and R[order[i]][j] > 0 and I[order[i]][k] > 0):
                        x, y = j, k
                storage_list.append((x, y))
            unique_storage_list = []
            seen_docker_types = set()
            for item in storage_list:
                _, docker_type = item
                if docker_type not in seen_docker_types:
                    unique_storage_list.append(item)
                    seen_docker_types.add(docker_type)
            alloc_flag = True
            for k in range(len(Q[0])):
                if I[order[i]][k] == 1 and alloc_flag:
                    alloc_flag = any(unique_storage_list[j][1] == k for j in range(len(unique_storage_list)))
            # 如果所有估值集合均满足约束条件，那么就进行扣除库存和赋值决策变量 x 的操作
            if alloc_flag:
                for server_id, docker_type in unique_storage_list:
                    if server_id != -1 and docker_type != -1 and I[order[i]][docker_type] == 1:
                        X[order[i]] = 1
                        Q[server_id][docker_type] -= 1
            print(X)
        return X, Q

    k = 0
    P = np.zeros(len(B))
    X = np.zeros(len(B))
    B1 = np.zeros((len(B)))
    m = len(B) // 25
    n = len(B) % 25
    for i in range(len(B)):
        B1[i] = sum([B[i][k] * I[i][k] for k in range(len(B[0]))])
    QQ = np.copy(Q)
    if len(B) >= 25:
        for i in range(m):
            order = [0] * 25
            count = 0
            while count < 25:
                order[count] = user_order[i * 25 + count]
                count = count + 1

            Q_A = np.copy(QQ)
            X, QQ = allocation(QQ, R, B1, I, order, P, X, d)
            P = payment(Q_A, R, B1, I, order, P, X, d)
    else:
        order = [0] * n
        for i in range(n):
            order[i] = user_order[m * 25 + i]
        Q_A = np.copy(QQ)
        X, QQ = allocation(QQ, R, B1, I, order, P, X, d)
        P = payment(Q_A, R, B1, I, order, P, X, d)

    print(P)
    print(X)
    return P, X


