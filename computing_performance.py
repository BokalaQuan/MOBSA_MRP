from algorithm.util import *

from scipy.stats.stats import ttest_ind

"""
Rand_Topo = ['Rand1', 'Rand2', 'Rand3', 'Rand4', 'Rand5', 'Rand6', 'Rand7', 'Rand8']
SNDlib_Topo = ['cost266', 'france', 'geant', 'germany50', 'india35', 'newyork', 
               'pioro40', 'ta1', 'ta2']
Zoo_Topo = ['AttMpls', 'Bellcanada', 'Bellsouth', 'BtNorthAmerica', 'Chinanet', 
            'Dfn', 'Geant2012', 'HiberniaGlobal', 'Highwinds', 'HurricaneElectric', 
            'Internetmci', 'Rediris', 'Tinet', 'Uninett2011', 'Uunet']
"""

if __name__ == '__main__':
    # topo_lst = ['Rand1', 'Rand2', 'Rand3', 'Rand4', 'Rand5', 'Rand6', 'Rand7', 'Rand8']
    # topo_lst = ['germany50', 'india35', 'ta1', 'ta2']
    topo_lst = ['AttMpls', 'BtNorthAmerica', 'HiberniaGlobal', 'Tinet']

    alst = ['NSABC', 'MOEA-PCGG', 'SPEA2', 'MOEAD', 'EAG-MOEAD', 'MOSFLA']
    # alst = ['MOEA-PCGG', 'NSGA-II', 'ENS-NDT']

    # titles = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8']
    # titles = ['S1', 'S2', 'S3', 'S4']
    titles = ['Z1', 'Z2', 'Z3', 'Z4']
    # titles = ['Rand-1', 'Rand-2', 'Rand-3', 'Rand-4', 'Rand-5', 'Rand-6', 'Rand-7', 'Rand-8']

    labels = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
    # labels = ['MOEA/PCG', 'NSGA-II', 'ENS-NDT']

    GD_lst = []
    IGD_lst = []
    HV_lst = []
    Epsilon_lst = []
    Spread_lst = []


    for topo in topo_lst[:]:
        GD_ = []
        IGD_ = []
        HV_ = []
        Epsilon_ = []
        Spread_ = []

        for al in alst[:]:
            GD, IGD, HV, Epsilon, Spread = read_metric(topo=topo, algorithm=al)
            GD_.append(GD)
            IGD_.append(IGD)
            HV_.append(HV)
            Epsilon_.append(Epsilon)
            Spread_.append(Spread)

        GD_lst.append(GD_)
        IGD_lst.append(IGD_)
        HV_lst.append(HV_)
        Epsilon_lst.append(Epsilon_)
        Spread_lst.append(Spread_)




        # print(topo)
        # print('IGD')
        # print(ttest_ind(IGD_[0], IGD_[1]))
        # print(ttest_ind(IGD_[0], IGD_[2]))
        # print(ttest_ind(IGD_[0], IGD_[3]))
        # print(ttest_ind(IGD_[0], IGD_[4]))
        # print(ttest_ind(IGD_[0], IGD_[5]))
        #
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        #
        # print(ttest_ind(IGD_[1], IGD_[2]))
        # print(ttest_ind(IGD_[1], IGD_[3]))
        # print(ttest_ind(IGD_[1], IGD_[4]))
        # print(ttest_ind(IGD_[1], IGD_[5]))
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        #
        # print("HV")
        # print(ttest_ind(HV_[0], HV_[1]))
        # print(ttest_ind(HV_[0], HV_[2]))
        # print(ttest_ind(HV_[0], HV_[3]))
        # print(ttest_ind(HV_[0], HV_[4]))
        # print(ttest_ind(HV_[0], HV_[5]))
        #
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        #
        #
        # print(ttest_ind(HV_[1], HV_[2]))
        # print(ttest_ind(HV_[1], HV_[3]))
        # print(ttest_ind(HV_[1], HV_[4]))
        # print(ttest_ind(HV_[1], HV_[5]))




    # boxplot(filename='Rand-GD1', lst=GD_lst, titles=titles[:4], labels=labels)
    # boxplot(filename='Rand-IGD1', lst=IGD_lst, titles=titles[:4], labels=labels)
    # boxplot(filename='Rand-HV1', lst=HV_lst, titles=titles[:4], labels=labels)
    #
    # boxplot(filename='Rand-GD2', lst=GD_lst, titles=titles[4:], labels=labels)
    # boxplot(filename='Rand-IGD2', lst=IGD_lst, titles=titles[4:], labels=labels)
    # boxplot(filename='Rand-HV2', lst=HV_lst, titles=titles[4:], labels=labels)
    #
    # boxplot(filename='S-GD', lst=GD_lst, titles=titles, labels=labels)
    # boxplot(filename='S-IGD', lst=IGD_lst, titles=titles, labels=labels)
    # boxplot(filename='S-HV', lst=HV_lst, titles=titles, labels=labels)
    #
    # boxplot(filename='Z-GD', lst=GD_lst, titles=titles, labels=labels)
    # boxplot(filename='Z-IGD', lst=IGD_lst, titles=titles, labels=labels)
    # boxplot(filename='Z-HV', lst=HV_lst, titles=titles, labels=labels)


    # boxplot(filename='R-GD1', lst=GD_lst[:4], titles=titles[:4], labels=labels)
    # boxplot(filename='R-Epsilon1', lst=Epsilon_lst[:4], titles=titles[:4], labels=labels)
    # boxplot(filename='R-Spread1', lst=Spread_lst[:4], titles=titles[:4], labels=labels)
    #
    # boxplot(filename='R-GD2', lst=GD_lst[4:], titles=titles[4:], labels=labels)
    # boxplot(filename='R-Epsilon2', lst=Epsilon_lst[4:], titles=titles[4:], labels=labels)
    # boxplot(filename='R-Spread2', lst=Spread_lst[4:], titles=titles[4:], labels=labels)

    # boxplot(filename='Rand-Epsilon1', lst=Epsilon_lst[:4], titles=titles[:4], labels=labels)
    # boxplot(filename='Rand-Spread1', lst=Spread_lst[:4], titles=titles[:4], labels=labels)
    #
    # boxplot(filename='Rand-Epsilon2', lst=Epsilon_lst[4:], titles=titles[4:], labels=labels)
    # boxplot(filename='Rand-Spread2', lst=Spread_lst[4:], titles=titles[4:], labels=labels)
    #
    # boxplot(filename='S-Epsilon', lst=Epsilon_lst, titles=titles, labels=labels)
    # boxplot(filename='S-Spread', lst=Spread_lst, titles=titles, labels=labels)

    boxplot(filename='Z-Epsilon', lst=Epsilon_lst, titles=titles, labels=labels)
    boxplot(filename='Z-Spread', lst=Spread_lst, titles=titles, labels=labels)


    # for topo in topo_lst[:]:
    #
    #     for al in alst[:]:
    #         print(topo, al)
    #         METRIC = cal_metric(topo=topo, runtime=20, algorithm=al)
    #         write_metric(topo=topo, algorithm=al, metric=METRIC)


        # plot_performance_as_boxplot(topo=topo, metric='GD', algorithms=alst, lst=GD_)
        # plot_performance_as_boxplot(topo=topo, metric='IGD', algorithms=alst, lst=IGD_)
        # plot_performance_as_boxplot(topo=topo, metric='HV', algorithms=alst, lst=HV_)
        #
        # print(IGD_)
        #
        # print(topo)
        # print(ttest_ind(IGD_[0], IGD_[1], equal_var=True))
        # print(ttest_ind(IGD_[0], IGD_[2], equal_var=True))
        # print(ttest_ind(IGD_[0], IGD_[3], equal_var=True))