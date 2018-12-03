#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
@author：Xiaoxue
@date: Sep 3rd, 2018


预定限额和保留水平的动态变化
注意这边输入的保留等级一定是从高价->低价
"""

from __future__ import division


def get_protection_levels(booking_limit, levels):
    """计算每个等级的保留水平

    参数：
        booking_limit: 每个等级的预定限额
        levels: 价格等级
    返回值:
        每个等级的保留水平

    例子:
        booking_limit = [100, 73, 72, 4, 0]
        levels = 5
        return
        res_lvl = [27, 88, 96, 100, 100]
    """
    max_demand = booking_limit[0]
    res_lvl = [max_demand - item for item in booking_limit[1:]]
    return res_lvl + [max_demand]


def get_booking_limit(res_lvl, levels):
    """计算每个等级的预定限额

    参数：
        res_lvl: 保留水平
        levels: 价格等级
    返回值:
        每个等级的预定限额

    例子:
        res_lvl = [27, 88, 96, 100, 100]
        levels = 5
        return [100, 73, 72, 4, 0]
    """
    max_demand = res_lvl[levels-1]
    booking_limit = [max_demand - item for item in res_lvl[0:-1]]
    booking_limit = [max_demand] + booking_limit
    return booking_limit


def request_seat(booking_limit, level, seat_class, seats_num):
    """计算每个请求是否被接受，接受后更新预定限额和保留水平，
        不接受请求返回现状

    参数：
        booking_limit: 预定限额
        levels: 价格等级
        seat_class: 请求的等级
        seat_num: 请求的座位数

    返回值:
        res_lvl: 更新后的保留水平
        booking_limit: 更新后的预定限额
        status: 是否接受该请求

    例子:
        res_lvl = [27, 88, 96, 100, 100]
        levels = 5
        seat_class = 1
        seat_num = 5
        return:
        booking_limit = [95, 73, 72, 4, 0],
        res_lvl = [22, 23, 91, 95, 95],
        status = 'Accept'
    """
    status = ('Reject' if booking_limit[seat_class] < seats_num else 'Accept')

    #更新状态
    if status == 'Accept':
        booking_limit = [item - seats_num if item > seats_num else 0 for item in booking_limit]
    return booking_limit, status


if __name__ == '__main__':
    res_lvl = [27, 88, 96, 100, 100]
    level = 5
    booking_limit = get_booking_limit(res_lvl, level)
    request_class_list = [4, 1, 1, 3, 2, 2, 2, 2, 2, 1, 2]
    request_num_list = [2, 5, 1, 1, 3, 4, 2, 4, 1, 2, 2]
    print('每个价格等级的保留量为：', res_lvl, '对应的限定水平为:', booking_limit)
    i = 1
    for seat_class, seats_num in zip(request_class_list, request_num_list):
        booking_limit, status = request_seat(booking_limit, level, seat_class, seats_num)
        print('第%d次请求:%d seats in Class %d 的状态为: %s' % (i, seats_num, seat_class, status))
        print('预定限额为:', booking_limit, '保留水平为:',
              get_protection_levels(booking_limit, level))
        i = i + 1
 """
 每个价格等级的保留量为： [27, 88, 96, 100, 100] 对应的限定水平为: [100, 73, 12, 4, 0]
第1次请求:2 seats in Class 4 的状态为: Reject
预定限额为: [100, 73, 12, 4, 0] 保留水平为: [27, 88, 96, 100, 100]
第2次请求:5 seats in Class 1 的状态为: Accept
预定限额为: [95, 68, 7, 0, 0] 保留水平为: [27, 88, 95, 95, 95]
第3次请求:1 seats in Class 1 的状态为: Accept
预定限额为: [94, 67, 6, 0, 0] 保留水平为: [27, 88, 94, 94, 94]
第4次请求:1 seats in Class 3 的状态为: Reject
预定限额为: [94, 67, 6, 0, 0] 保留水平为: [27, 88, 94, 94, 94]
第5次请求:3 seats in Class 2 的状态为: Accept
预定限额为: [91, 64, 3, 0, 0] 保留水平为: [27, 88, 91, 91, 91]
第6次请求:4 seats in Class 2 的状态为: Reject
预定限额为: [91, 64, 3, 0, 0] 保留水平为: [27, 88, 91, 91, 91]
第7次请求:2 seats in Class 2 的状态为: Accept
预定限额为: [89, 62, 1, 0, 0] 保留水平为: [27, 88, 89, 89, 89]
第8次请求:4 seats in Class 2 的状态为: Reject
预定限额为: [89, 62, 1, 0, 0] 保留水平为: [27, 88, 89, 89, 89]
第9次请求:1 seats in Class 2 的状态为: Accept
预定限额为: [88, 61, 0, 0, 0] 保留水平为: [27, 88, 88, 88, 88]
第10次请求:2 seats in Class 1 的状态为: Accept
预定限额为: [86, 59, 0, 0, 0] 保留水平为: [27, 86, 86, 86, 86]
第11次请求:2 seats in Class 2 的状态为: Reject
预定限额为: [86, 59, 0, 0, 0] 保留水平为: [27, 86, 86, 86, 86]
 """

