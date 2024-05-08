import numpy as np
from data import generate_dataset
from OPT import opt

# 该算法为OPAA算法 将静态模型OPT的最优分配计算出来，通过最优分配，我们可以通过梯度下降算法对loss函数（是关于价格p的函数）进行收敛，从而获得价格矩阵P

def opaa(Q, R, B, d):
    def calculate_utility(prices, B, x):
        num_users = len(B)
        num_servers = len(prices)
        num_docker_types = len(prices[0])

        utility = np.zeros(num_users)
        for i in range(num_users):
            sum = 0
            for j in range(num_servers):
                for k in range(num_docker_types):
                    if (B[i][k] * x[i][j][k] - prices[j][k] * x[i][j][k] > 0):
                        sum += B[i][k] * x[i][j][k] - prices[j][k] * x[i][j][k]

            utility[i] = sum

        return utility

    def update_prices(prices, B, x, Q, learning_rate):
        num_servers = len(prices)
        num_docker_types = len(prices[0])
        num_users = len(B)

        all_loss_small = False  # 初始化标志变量为 False

        while not all_loss_small:
            utility = calculate_utility(prices, B, x)
            all_loss_small = True  # 每次循环开始时将标志变量设为 True
            for j in range(num_servers):
                for k in range(num_docker_types):
                    total_utility = 0
                    num_x = 0
                    for i in range(num_users):
                        if x[i][j][k] == 1:
                            total_utility += utility[i]

            loss = sum(
                (sum(x[i][j][k] * (B[i][k] - prices[j][k]) for i in range(num_users)) - prices[j][k] * Q[j][k]) ** 2
                for j in range(num_servers) for k in range(num_docker_types))
            print(loss)
            if abs(loss) >= 1e-6:
                all_loss_small = False  # 如果有任何一个元素的损失函数大于等于 1e-6，则将标志变量设为 False
                for j in range(num_servers):
                    for k in range(num_docker_types):
                        num_x = 0
                        for i in range(num_users):
                            if x[i][j][k] == 1:
                                num_x += 1
                                total_utility += utility[i]
                        gradient = 2 * (
                                    sum(x[i][j][k] * (B[i][k] - prices[j][k]) for i in range(num_users)) - prices[j][
                                k] * Q[j][k]) * (-num_x - Q[j][k])
                        # gradient = total_utility + Q[j][k]
                        prices[j][k] -= learning_rate * gradient
                        # print(prices[j][k])

        return prices

    def main():

        num_users = len(B)
        num_servers = len(Q)
        num_docker_types = len(Q[0])
        prices = np.zeros((num_servers, num_docker_types))

        learning_rate = 0.001
        x1 = opt(Q, R, B, d)

        prices = update_prices(prices, B, x1, Q, learning_rate)
        utility = calculate_utility(prices, B, x1)
        servers_utility = 0
        users_utility = 0
        for i in range(num_users):
            for j in range(num_servers):
                for k in range(num_docker_types):
                    servers_utility += prices[j][k] * x1[i][j][k]
            users_utility += utility[i]
        print("Final Prices:")
        print(prices)
        print("Utility:", utility)
        print("servers_utility:", servers_utility)
        print("users_utility:", users_utility)

        return prices, x1

    p, x = main()
    return p, x




R = [[0, 1], [1,  0], [1, 1]]  # 用户i对于服务器 j 是否可以连接（部署约束）用Rij 表示，Rij =1表示可以连接。
B = [[7, 3], [4, 4], [3, 8]]  # 用户 i 对 k 类型 docker 的估值可以用vik 表示
Q = [[1, 1], [1, 1]]  # 每个 EQS 拥有的 docker 个数
d = 2
p, x=opaa(Q, R, B, d)
print(p)