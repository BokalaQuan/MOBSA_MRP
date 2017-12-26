import os
import json
import random

PATH = os.path.split(os.path.realpath(__file__))[0]

class MultiObjectiveKnapsackProblem(object):
    '''
    MOKP
    '''
    def __init__(self):
        self.mokp = []

        self.num_item = 0
        self.num_knap = 0


    def initialize(self, filename):
        FILE_PATH = PATH + '/data/' + filename
        with open(FILE_PATH, 'r') as f:
            conf = json.load(f)
            for item in conf:
                self.mokp.append(item)
            f.close()

        self.num_item = len(self.mokp[0]['items'])
        self.num_knap = len(self.mokp)


    def create_problem(self, num_knapsacks, num_items):
        item_weight = []
        item_profit = []
        item_ratio = []
        knap_capacity = []

        self.num_item = num_items
        self.num_knap = num_knapsacks


        for x in range(num_knapsacks):
            sum = 0
            weight_list = []
            profit_list = []
            ratio_list = []

            for i in range(num_items):
                weight = int(random.uniform(1, 100))
                profit = int(random.uniform(1, 100))

                weight_list.append(weight)
                profit_list.append(profit)
                ratio_list.append(float('%.2f' % (float(profit) / weight)))

                sum += weight

            item_weight.append(weight_list)
            item_profit.append(profit_list)
            item_ratio.append(ratio_list)
            knap_capacity.append(sum / 2)

        for x in range(2):
            item_dict = self.to_dict_item(item_weight[x], item_profit[x], item_ratio[x])
            knap_dict = self.to_dict_knap(x + 1, item_dict, knap_capacity[x])

            self.mokp.append(knap_dict)

        self.save_problem(self.mokp)

    def save_problem(self, dict):
        FILE_PATH = PATH + "/data/" + str(self.num_item) + "_" + str(self.num_knap) + ".json"

        with open(FILE_PATH, 'wb') as f:
            f.write(json.dumps(dict, indent=4, sort_keys=True))

            print "File OK."

    @staticmethod
    def to_dict_knap(index_knapsack, item, capacity):

        return {'knapsack': index_knapsack,
                'capacity': capacity,
                'items': item}

    @staticmethod
    def to_dict_item(item_weight, item_profit, item_ratio):

        item_list = []
        for x in range(len(item_profit)):
            item = {}
            item['item'] = x
            item['profit'] = item_profit[x]
            item['weight'] = item_weight[x]
            item['ratio'] = item_ratio[x]
            item_list.append(item)

        return item_list

if __name__ == '__main__':
    test = MultiObjectiveKnapsackProblem()
    test.create_problem(2,500)
