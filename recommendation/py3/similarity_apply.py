import collections
import similarity as core


# 获得某item的所有相似东西
def get_top_matches(item_id, all_infos, n=5, similarity=core.sim_pearson):
    scores = [(
        similarity(all_infos[item_id], all_infos[other_id]), other_id
    ) for other_id in all_infos if other_id != item_id]

    scores.sort()
    scores.reverse()
    return scores[0: n]


# 基于主体相似集，向主体推荐客体
def get_recommendations(subj_id, all_infos, n=5, similarity=core.sim_pearson):
    """
    若subject为人，则得出该人最可能喜欢的物品
    若subject为物，则得出最可能喜欢该物品的人
    """
    totals = collections.defaultdict(int)
    sim_sums = collections.defaultdict(int)
    subj_prefs = all_infos[subj_id]
    for other, other_perfs in all_infos.items():
        if other == subj_id:
            continue
        sim = similarity(subj_prefs, other_perfs)
        if sim <= 0:  # 兴趣不相符的直接过滤掉
            continue
        for obj in other_perfs:
            if obj not in subj_prefs or subj_prefs[obj] == 0:
                totals[obj] += other_perfs[obj] * sim
                sim_sums[obj] += sim
    rankings = [(score/sim_sums[obj], obj) for obj, score in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


# 基于客体相似集，向主体推荐客体
def get_recommend_items(pref, sim_infos, n=5, similarity=core.sim_pearson):
    """
    若subject为人，则得出该人最可能喜欢的物品
    若subject为物，则得出最可能喜欢该物品的人
    """
    scores = collections.defaultdict(int)
    total_sim = collections.defaultdict(int)

    for (item, score) in pref.items():
        for (similarity, item2) in sim_infos[item]:
            if item2 in pref:
                continue
            scores[item2] += similarity * score
            total_sim[item2] += similarity
    rankings = [
        (scores/total_sim[item], item) for item, scores in scores.items()]

    rankings.sort()
    rankings.reverse()
    return rankings


# 工具：反转字典：评价者，被评价物交换
def transform_preferences(pres):
    result = collections.defaultdict(dict)
    for person in pres:
        for item in pres[person]:
            result[item][person] = pres[person][item]
    return result


# 寻找相似物品
def calculate_similar_items(preferences, n=10):
    result = {}

    item_preferences = transform_preferences(preferences)
    c = 0
    for item in item_preferences:
        # 进度统计
        c += 1
        if c % 100 == 0:
            print('{} / {}'.format(c, len(item_preferences)))
        # 汇总所有
        scores = get_top_matches(item, item_preferences,
                                 n=n, similarity=core.sim_distance)
        result[item] = scores
    return result


if __name__ == '__main__':
    # 嵌套字典。用户偏好，用户为key，偏好为value
    # value中，被评价物品为key,评价分数为value
    critics = {
        'Lisa Rose': {
            'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
            'Just My Luck': 3.0, 'Superman Returns': 3.5,
            'You, Me and Dupree': 2.5, 'The Night Listener': 3.0
        },
        'Gene Seymour': {
            'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
            'Just My Luck': 1.5, 'Superman Returns': 5.0,
            'The Night Listener': 3.0, 'You, Me and Dupree': 3.5
        },
        'Michael Phillips': {
            'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
            'Superman Returns': 3.5, 'The Night Listener': 4.0
        },
        'Claudia Puig': {
            'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
            'The Night Listener': 4.5, 'Superman Returns': 4.0,
            'You, Me and Dupree': 2.5
        },
        'Mick LaSalle': {
            'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
            'Just My Luck': 2.0, 'Superman Returns': 3.0,
            'The Night Listener': 3.0, 'You, Me and Dupree': 2.0
        },
        'Jack Matthews': {
            'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
            'The Night Listener': 3.0, 'Superman Returns': 5.0,
            'You, Me and Dupree': 3.5
        },
        'Toby': {
            'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0,
            'Superman Returns': 4.0
        }
    }
    print(get_top_matches('Lisa Rose', critics))

    print(get_recommendations('Toby', critics))

    sim_infos = calculate_similar_items(critics)
    print(get_recommend_items(critics['Toby'], sim_infos))
