import random

class A(object):

    def __init__(self):
        self.value = random.randint(-10, 10)

    def __repr__(self):
        return 'id :' + str(id(self)) + 'value :' + str(self.value)

    def __str__(self):
        return 'id :' + str(id(self)) + ' value :' + str(self.value)

    def __eq__(self, other):
        if self.value == other.value:
            return True
        return False

    def __lt__(self, other):
        if self.value < other.value:
            return True
        return False

    def __gt__(self, other):
        if self.value > other.value:
            return True
        return False

    def __dict__(self):
        return {'value': self.value}

if __name__ == '__main__':
    ll = [A() for i in range(5)]

    for item in ll:
        print item


    # ll = [A() for i in range(10)]
    # for x in ll:
    #     print x.value
    #
    # ll.sort(cmp=None, key=lambda x:x.value, reverse=False)
    #
    # for x in ll:
    #     print x.value

    #
    # aa = [random.randint(-10, 10) for i in range(10)]
    # bb = []
    #
    # aa.sort()
    # print aa
    #
    # for j in range(len(aa)-1, -1-5, -1):
    #     if aa[j] > 0:
    #         bb.append(aa.pop(j))
    #         print j
    #
    # print aa
    # print bb
