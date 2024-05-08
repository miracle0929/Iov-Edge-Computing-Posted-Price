import numpy as np
from docplex.mp.model import Model
from data import get_dataset, generate_dataset
import random
from temp import compute
from temp import off_compute
import matplotlib.pyplot as plt
from docplex.cp.model import *
from OPT import opt
from OPT_P import opt_p
from Posted_Price import opaa
from Fixed_price import fix_price
from ODRAP import odrap
from allocation import alg_assign


def price1(Q, R, B, I, user, d):
    T1, N1, H1, U1, W1, O1 = 0, 0, 0, 0, 0, 0
    T2, N2, H2, U2, W2, O2 = 0, 0, 0, 0, 0, 0
    T3, N3, H3, U3, W3, O3 = 0, 0, 0, 0, 0, 0
    T4, N4, H4, U4, W4, O4 = 0, 0, 0, 0, 0, 0

    p, x = opaa(Q, R, B, d)
    fix_p1 = fix_price(Q, R, B)
    p1, x3 = opt_p(Q, R, B, p, d)

    for i in range(5):
        QQ = np.copy(Q)
        user_ord = random.sample(range(user), user)
        x1 = alg_assign(R, Q, p, B, user_ord, d)
        x2 = alg_assign(R, Q, fix_p1, B, user_ord, d)
        online, x6 = odrap(Q, R, B, I, user_ord, d)
        payments1, total_utility1, Servers_utility1, users_utility1, winner_counts1, docker_utilization1 = compute(Q, R,
                                                                                                                   B, p,
                                                                                                                   x1)
        payments2, total_utility2, Servers_utility2, users_utility2, winner_counts2, docker_utilization2 = compute(Q, R,
                                                                                                                   B,
                                                                                                                   fix_p1,
                                                                                                                   x2)
        payments3, total_utility3, Servers_utility3, users_utility3, winner_counts3, docker_utilization3 = compute(Q, R,
                                                                                                                   B,
                                                                                                                   p1,
                                                                                                                   x3)
        payments4, total_utility4, Servers_utility4, users_utility4, winner_counts4, docker_utilization4 = off_compute(
            Q, R, B, I, online, x6)
        T1 += payments1
        N1 += total_utility1
        H1 += Servers_utility1
        U1 += users_utility1
        W1 += winner_counts1
        O1 += docker_utilization1
        T2 += payments2
        N2 += total_utility2
        H2 += Servers_utility2
        U2 += users_utility2
        W2 += winner_counts2
        O2 += docker_utilization2
        T3 += payments3
        N3 += total_utility3
        H3 += Servers_utility3
        U3 += users_utility3
        W3 += winner_counts3
        O3 += docker_utilization3
        T4 += payments4
        N4 += total_utility4
        H4 += Servers_utility4
        U4 += users_utility4
        W4 += winner_counts4
        O4 += docker_utilization4
    payments1, total_utility1, Servers_utility1, users_utility1, winner_counts1, docker_utilization1 = T1 / 5, N1 / 5, H1 / 5, U1 / 5, W1 / 5, O1 / 5
    payments2, total_utility2, Servers_utility2, users_utility2, winner_counts2, docker_utilization2 = T2 / 5, N2 / 5, H2 / 5, U2 / 5, W2 / 5, O2 / 5
    payments3, total_utility3, Servers_utility3, users_utility3, winner_counts3, docker_utilization3 = T3 / 5, N3 / 5, H3 / 5, U3 / 5, W3 / 5, O3 / 5
    payments4, total_utility4, Servers_utility4, users_utility4, winner_counts4, docker_utilization4 = T4 / 5, N4 / 5, H4 / 5, U4 / 5, W4 / 5, O4 / 5

    payments = [payments1, payments2, payments3, payments4]
    total_utility = [total_utility1, total_utility2, total_utility3, total_utility4]
    Servers_utility = [Servers_utility1, Servers_utility2, Servers_utility3, Servers_utility4]
    users_utility = [users_utility1, users_utility2, users_utility3, users_utility4]
    winner_count = [winner_counts1, winner_counts2, winner_counts3, winner_counts4]
    docker_utilization = [docker_utilization1, docker_utilization2, docker_utilization3, docker_utilization4]
    return payments, total_utility, Servers_utility, users_utility, winner_count, docker_utilization


dataset = generate_dataset(200, 7, 5, 3)
Q1, R1, B1, I1 = get_dataset(dataset, 10, 3)
Q2, R2, B2, I2 = get_dataset(dataset, 20, 3)
Q3, R3, B3, I3 = get_dataset(dataset, 50, 3)
Q4, R4, B4, I4 = get_dataset(dataset, 100, 3)
Q5, R5, B5, I5 = get_dataset(dataset, 200, 3)

payments1, total_utility1, Servers_utility1, users_utility1, winner_count1, docker_utilization1 = price1(Q1, R1, B1, I1,
                                                                                                         10, 3)

payments2, total_utility2, Servers_utility2, users_utility2, winner_count2, docker_utilization2 = price1(Q2, R2, B2, I2,
                                                                                                         20, 3)
#
payments3, total_utility3, Servers_utility3, users_utility3, winner_count3, docker_utilization3 = price1(Q3, R3, B3, I3,
                                                                                                         50, 3)
payments4, total_utility4, Servers_utility4, users_utility4, winner_count4, docker_utilization4 = price1(Q4, R4, B4, I4,
                                                                                                         100, 3)
#
payments5, total_utility5, Servers_utility5, users_utility5, winner_count5, docker_utilization5 = price1(Q5, R5, B5, I5,
                                                                                                         200, 3)
payments = [payments1, payments2, payments3, payments4, payments5]
total_utility = [total_utility1, total_utility2, total_utility3, total_utility4, total_utility5]
Servers_utility = [Servers_utility1, Servers_utility2, Servers_utility3, Servers_utility4, Servers_utility5]
winner_count = [winner_count1, winner_count2, winner_count3, winner_count4, winner_count5]
users_utility = [users_utility1, users_utility2, users_utility3, users_utility4, users_utility5]
docker_utilization = [docker_utilization1, docker_utilization2, docker_utilization3, docker_utilization4,
                      docker_utilization5]
print("total_utility:")
print(total_utility)
print("Servers_utility:")
print(Servers_utility)
print("winner_count:")
print(winner_count)
print("users_utility:")
print(users_utility)

with open("data_user_number.txt", "w") as file:
    file.write("posted_price:\n")
    file.write("payments:")
    for i in range(len(payments)):
        file.write(str(payments[i][0]) + ",")
    file.write("\ntotal_utility:")
    for i in range(len(payments)):
        file.write(str(total_utility[i][0]) + ",")
    file.write("\nServers_utility:")
    for i in range(len(payments)):
        file.write(str(Servers_utility[i][0]) + ",")
    file.write("\nwinner_count:")
    for i in range(len(payments)):
        file.write(str(winner_count[i][0]) + ",")
    file.write("\nusers_utility:")
    for i in range(len(payments)):
        file.write(str(users_utility[i][0]) + ",")
    file.write("\ndocker_utilization:")
    for i in range(len(payments)):
        file.write(str(docker_utilization[i][0]) + ",")
    file.write("\n\n")

    file.write("fixed_price:\n")
    file.write("payments:")
    for i in range(len(payments)):
        file.write(str(payments[i][1]) + " ")
    file.write("\ntotal_utility:")
    for i in range(len(payments)):
        file.write(str(total_utility[i][1]) + ",")
    file.write("\nServers_utility:")
    for i in range(len(payments)):
        file.write(str(Servers_utility[i][1]) + ",")
    file.write("\nwinner_count:")
    for i in range(len(payments)):
        file.write(str(winner_count[i][1]) + ",")
    file.write("\nusers_utility:")
    for i in range(len(payments)):
        file.write(str(users_utility[i][1]) + ",")
    file.write("\ndocker_utilization:")
    for i in range(len(payments)):
        file.write(str(docker_utilization[i][1]) + ",")
    file.write("\n\n")

    file.write("OPT_P:\n")
    file.write("payments:")
    for i in range(len(payments)):
        file.write(str(payments[i][2]) + " ")
    file.write("\ntotal_utility:")
    for i in range(len(payments)):
        file.write(str(total_utility[i][2]) + ",")
    file.write("\nServers_utility:")
    for i in range(len(payments)):
        file.write(str(Servers_utility[i][2]) + ",")
    file.write("\nwinner_count:")
    for i in range(len(payments)):
        file.write(str(winner_count[i][2]) + ",")
    file.write("\nusers_utility:")
    for i in range(len(payments)):
        file.write(str(users_utility[i][2]) + ",")
    file.write("\ndocker_utilization:")
    for i in range(len(payments)):
        file.write(str(docker_utilization[i][2]) + ",")
    file.write("\n\n")

    file.write("ODRAP:\n")
    file.write("payments:")
    for i in range(len(payments)):
        file.write(str(payments[i][3]) + " ")
    file.write("\ntotal_utility:")
    for i in range(len(payments)):
        file.write(str(total_utility[i][3]) + ",")
    file.write("\nServers_utility:")
    for i in range(len(payments)):
        file.write(str(Servers_utility[i][3]) + ",")
    file.write("\nwinner_count:")
    for i in range(len(payments)):
        file.write(str(winner_count[i][3]) + ",")
    file.write("\nusers_utility:")
    for i in range(len(payments)):
        file.write(str(users_utility[i][3]) + ",")
    file.write("\ndocker_utilization:")
    for i in range(len(payments)):
        file.write(str(docker_utilization[i][3]) + ",")
    file.write("\n\n")

