import numpy as np


def alg_assign(R, QQ, p, B, user_order, d):
    num_servers, num_docker_types = len(QQ), len(QQ[0])
    num_users = len(B)
    Q = np.copy(QQ)
    task_list = user_order.copy()
    x1 = [[[0 for _ in range(num_docker_types)] for _ in range(num_servers)] for _ in range(num_users)]

    for user in task_list:

        x = -1
        y = -1
        value = 0
        storage_list = []  # 存储服务器ID和Docker类型的列表

        for docker_type in range(len(B[0])):
            if B[user][docker_type] != 0:
                max_value = 0
                for server_id in range(len(R[0])):
                    if (Q[server_id][docker_type] > 0 and R[user][server_id] > 0 and B[user][docker_type] -
                            p[server_id][docker_type] > max_value):
                        max_value = B[user][docker_type] - p[server_id][docker_type]
                        x, y = server_id, docker_type
                value = max_value
                storage_list.append((x, y, value))
        # 只保留每个 Docker 类型的唯一元素

        unique_storage_list = []
        seen_docker_types = set()
        for item in storage_list:
            _, docker_type, _ = item
            if docker_type not in seen_docker_types:
                unique_storage_list.append(item)
                seen_docker_types.add(docker_type)
        unique_storage_list = sorted(unique_storage_list, key=lambda item: item[2], reverse=True)
        count = 0
        # 如果所有估值集合均满足约束条件，那么就进行扣除库存和赋值决策变量 x 的操作
        for server_id, docker_type, _ in unique_storage_list:
            if server_id != -1 and docker_type != -1 and count < d:
                Q[server_id][docker_type] -= 1
                x1[user][server_id][docker_type] = 1
                count = count + 1
        print(storage_list)
    return x1