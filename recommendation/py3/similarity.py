from math import sqrt


def sim_distance(user1_prefs, user2_prefs):
    """
    欧几里得距离：计算整体相似度
    :param user1_prefs: 用户1的兴趣字典 {'hobby_1': 'score_1'}
    :param user2_prefs: 用户1的兴趣字典 {'hobby_1': 'score_2'}
    :return: 用户兴趣相似度，越相似值越趋向于1
    """
    # 若无共同兴趣，返回0
    si = {}
    for item in user1_prefs:
        if item in user2_prefs:
            si[item] = 1
    if len(si) == 0:
        return 0

    # 计算欧几里得距离
    sum_of_squares = sum([
        pow(user1_prefs[item] - user2_prefs[item], 2)
        for item in user1_prefs if item in user2_prefs
    ])

    # 规范化
    return 1/(1+sum_of_squares)


def sim_pearson(user1_prefs, user2_prefs):
    """
    皮尔逊相关度：计算二者对物品喜爱的相关度 （亦即概率论中的相关系数：协方差/标准差 ）
    :param user1_prefs: 用户1的兴趣字典 {'hobby_1': 'score_1'}
    :param user2_prefs: 用户1的兴趣字典 {'hobby_1': 'score_2'}
    :return: 返回值介于-1到1之间，兴趣越相似，越接近于1 兴趣恰好相反，则为-1.
    """
    si = {}
    for item in user1_prefs:
        if item in user2_prefs:
            si[item] = 1
    n = len(si)
    # 二者没有相同处时，则二者兴趣无相关
    if n == 0:
        return 0

    # 偏好求和
    sum1 = sum([user1_prefs[it] for it in si])
    sum2 = sum([user2_prefs[it] for it in si])

    # 求平方和
    sum1_sq = sum([pow(user1_prefs[it], 2) for it in si])
    sum2_sq = sum([pow(user2_prefs[it], 2) for it in si])

    # 求乘积之和
    sum_p = sum([user1_prefs[it] * user2_prefs[it] for it in si])

    # 计算皮尔逊评价值
    num = sum_p - (sum1*sum2/n)
    den = sqrt((sum1_sq - pow(sum1, 2)/n)*(sum2_sq - pow(sum2, 2)/n))
    if den == 0:
        return 0

    r = num/den
    return r
