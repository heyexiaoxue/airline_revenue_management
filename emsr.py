"""期望边际座位收益（EMSR）启发算法

EMSR-a：使用Littlewood法则计算当前等级相对于每一个更高等级的保留水平
        假设条件是：每个价格的需求量都是满足正态分布的

EMSR-b: 假设被一个额外预定所替代的乘客支付的票价，等于未来票价的加权平均值
        EMSRb创造了一个“人造等级”，该等级的需求等于未来所有周期的需求之和，
        该等级的票价等于未来所有预定的平均期望票价
        然后，使用LittleWood法则计算当前等级j相对该人造等级的预定限额
"""

from __future__ import division
import numpy as np
from scipy.stats import norm
import math


def emsr_a(mu, sigma, demand_prices, demand_classes, cap):
    """计算所有等级的保留结果

    参数：
        mu: 每个等级对应的需求均值列表
        sigma: 每个等级对应的需求标准差列表
        demand_prices: 每个等级对应的价格
        demand_classes: 等级数，其中等级0为最高等级，也就是高价，
                        其他等级依次递减，直到等级demand_classes-1，
                        等级demand_classes-1为最低价
        cap: 表示航班的包机数

    返回值：每个等级的保留水平
           例子：
            emsr-a:  [9.706804042642494, 50.460693186249436, 91.63169552684437]
    """
    return [calculate_protect_revenue_a(j, mu, sigma, demand_prices, cap)
            for j in range(0, demand_classes-1)
            ]


def calculate_protect_revenue_a(j, mu, sigma, demand_prices, cap):
    """计算第i等级的保留水平"""
    revenue_j = sum([calculate_protect_single_item(mu[i], sigma[i],
                                                   1. - demand_prices[j+1] * 1.0 / demand_prices[i])
                     for i in range(0, j+1)])
    return min(revenue_j, cap)


def calculate_protect_single_item(scalar_mu, scalar_sigma, prob):
    """计算每个等级的子项的贡献值"""
    return scalar_mu + scalar_sigma * norm.ppf(prob)


def emsr_b(mu, sigma, demand_prices, demand_classes, cap):
    """计算所有等级的保留结果

    参数：
        mu: 每个等级对应的需求均值列表
        sigma: 每个等级对应的需求标准差列表
        demand_prices: 每个等级对应的价格
        demand_classes: 等级数，其中等级0为最高等级，也就是高价，
                        其他等级依次递减，直到等级demand_classes-1，
                        等级demand_classes-1为最低价
        cap: 表示航班的包机数

    返回值：每个等级的保留水平
           例子：
            EMSR-b:  [9.706804042642494, 53.267964550034094, 96.83465042758874]
    """
    return [calculate_protect_revenue_b(j, mu, sigma, demand_prices, cap)
            for j in range(1, demand_classes)
            ]


def calculate_protect_revenue_b(j, mu, sigma, demand_prices, cap):
    """计算第j等级的保留水平"""
    new_mu = sum(mu[:j]) * 1.0
    # 计算前j-1的mu值和
    new_sigma = math.sqrt(sum([item * item for item in sigma[:j]]))
    # 计算前j-1个方差和的标准差
    new_price = sum([item_mu * item_p * 1.0 / new_mu
                     for item_mu, item_p in zip(mu[:j], demand_prices[:j])])
    # 计算前j-1个价格*均值mu/新的均值作为新的人造等级的价格
    return min(cap, calculate_protect_single_item(new_mu, new_sigma,
                                                  1 - demand_prices[j] / new_price))

def emsr_revise(mu, sigma, demand_prices, demand_classes, cap, alpha):
    """计算所有等级的保留结果

    参数：
        mu: 每个等级对应的需求均值列表
        sigma: 每个等级对应的需求标准差列表
        demand_prices: 每个等级对应的价格
        demand_classes: 等级数，其中等级0为最高等级，也就是高价，
                        其他等级依次递减，直到等级demand_classes - 1，
                        等级demand_classes - 1为最低价
        cap: 表示航班的包机数
        alpha: 表示顾客向上购买的因子参数，且alpha < 1.

    返回值：每个等级的保留水平
           例子：
            emsr-a:  [9.706804042642494, 50.460693186249436, 91.63169552684437]

"""
    return [calculate_protect_revenue_revise(j, mu, sigma, demand_prices, cap, alpha)
            for j in range(1, demand_classes)
            ]


def calculate_protect_revenue_revise(j, mu, sigma, demand_prices, cap, alpha):
    """计算第j等级的保留水平"""
    new_mu = sum(mu[:j]) * 1.0
    # 计算前j-1的mu值和
    new_sigma = math.sqrt(sum([item * item for item in sigma[:j]]))
    # 计算前j-1个方差和的标准差
    new_price = sum([item_mu * item_p * 1.0 / new_mu
                     for item_mu, item_p in zip(mu[:j], demand_prices[:j])])
    # 计算前j-1个价格*均值mu/新的均值作为新的人造等级的价格
    return min(cap, calculate_protect_single_item(new_mu, new_sigma,
                                                  (1 - demand_prices[j] / new_price))/(1-alpha))

if __name__ == "__main__":
    levels = 4
    prices = [1050, 950, 699, 520]
    demand_mus = [17.3, 45.1, 39.6, 34.0]
    demand_sigmas = [5.8, 15.0, 13.2, 11.3]
    cap = 100
    alpha = 0.05

    res_lvl_a = emsr_a(demand_mus, demand_sigmas, prices, levels, cap)
    res_lvl_b = emsr_b(demand_mus, demand_sigmas, prices, levels, cap)
    res_lvl_revise = emsr_revise(demand_mus, demand_sigmas, prices, levels, cap,alpha)
    print("EMSR-a: ", res_lvl_a)
    print("EMSR-b: ", res_lvl_b)
    print("EMSR-revise: ", res_lvl_revise)

"""
结果
EMSR-a:  [9.706804042642494, 50.460693186249436, 91.63169552684437]
EMSR-b:  [9.706804042642494, 53.267964550034094, 96.83465042758874]
EMSR-revise:  [10.217688465939467, 56.071541631614835, 100]
"""


