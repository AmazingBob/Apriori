import numpy as np


class Apriori(object):
    def __init__(self):
        self.freq_set = []  # 频繁项集
        return

    def fit(self, database, threshold):
        """
        计算最大频繁项集
        :param database: 数据库
        :param threshold: 阈值
        :return:
        """
        self.database = database
        if len(database) == 0:
            return []
        for event in database:
            for item in event:
                if [item] not in self.freq_set:
                    self.freq_set.append([item])
        self.__update_sup__()
        while (len(self.freq_set) > 1):
            self.__cut__(threshold)
            self.__concentrate__()
        if len(self.freq_set) == 0:
            print("None")
            return
        print(self.freq_set[0], self.__sup[0])
        return

    def __concentrate__(self):
        """
        更新频繁项集
        :return:
        """
        length = len(self.freq_set)
        if length == 1:
            return
        new_set = []
        for i in range(length):
            for j in range(i + 1, length):
                event_1 = self.freq_set[i]
                event_2 = self.freq_set[j]
                union = set(event_1).union(set(event_2))
                if union in new_set:
                    continue
                new_set.append(union)
        self.freq_set = new_set
        self.__update_sup__()
        return

    def __update_sup__(self):
        """
        更新支持度
        :return:
        """
        self.__sup = []
        for event_c in self.freq_set:
            sup = 0.
            for event_b in self.database:
                intersection = [item for item in event_c if item in event_b]
                if len(intersection) == len(event_c):
                    sup = sup + 1
            self.__sup.append(sup)
        self.__sup = np.array(self.__sup, dtype=np.float32)
        self.__sup = self.__sup / len(self.database)
        return

    def __cut__(self, threshold):
        """
        剪枝，删除支持度小于阈值的项集。
        :param threshold: 阈值
        :return:
        """
        new_set = []
        new_sup = []
        for index in range(len(self.__sup)):
            if self.__sup[index] >= threshold:
                new_set.append(self.freq_set[index])
                new_sup.append(self.__sup[index])
        self.__sup = new_sup
        self.freq_set = new_set
        return


if __name__ == '__main__':
    # 数据库
    database = [["面包", "牛奶", "啤酒", "尿布"],
                ["面包", "牛奶", "啤酒"],
                ["啤酒", "尿布"],
                ["面包", "牛奶", "花生"]]
    apr = Apriori()
    apr.fit(database, 0.7)
    pass
