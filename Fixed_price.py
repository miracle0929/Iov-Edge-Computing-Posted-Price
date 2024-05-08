
# 该代码为固定价格算法
# 算法思路为 将所有用户对某个docker的估值累加起来再除以对这个docker有估值的用户总数 的0.15倍作为定价
# 用户对docker有估值并不代表必须购买该商品，所以对估值累加起来的溢价过高，对其乘以0.15倍进行均衡

def fix_price(Q, R, B):
    num_users = len(B)
    num_servers = len(Q)
    num_docker_types = len(Q[0])
    price = [0] * num_docker_types
    B1 = [[0] * num_docker_types] * num_servers
    # 计算出所有用户对docker的均值 并且取1/2

    for k in range(num_docker_types):
        sum = 0
        count = 0
        for i in range(num_users):
            if B[i][k] != 0:
                sum += B[i][k]
                count += 1
        if count != 0:
            price[k] = (sum / count) * 0.15
    for j in range(num_servers):
        for k in range(num_docker_types):
            B1[j][k] = price[k]

    return B1
