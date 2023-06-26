from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.metrics import precision_score
from db import DB
import pandas as pd
from datetime import date

today = date.today()
d1 = today.strftime("%d.%m.%Y")
print(d1)
database = DB()


class Fix:
    def __init__(self):
        self.data_all = []
        self.columns = []
        self.columns_long = []
        self.test_days = []
        self.train = pd.DataFrame()
        self.test = pd.DataFrame()
        self.org_test = pd.DataFrame()

    def main(self):
        # database = DB()
        data_all = database.main()
        self.data_all = data_all
        test_days = self.day_select()
        self.test_days = test_days
        self.columns = database.columns
        self.columns_long = database.columns_long
        train, test, org_test = self.separate()
        train.columns = self.columns
        if len(test) > 0:
            test.columns = self.columns
            org_test.columns = self.columns_long
        self.train = train
        self.test = test
        self.org_test = org_test
        # print('fix main done')

    def day_select(self):
        data = self.data_all
        week_last = data[len(data) - 1]['Hafta']
        last_week_bef = week_last - 1
        bound_up = len(data) - 1
        test_days = []

        for rows in (range(bound_up, -1, -1)):
            data_ = list(data[rows].values())
            # print(data_)
            if data_[1] == week_last or data_[1] == last_week_bef:
                if data_[3] != d1:
                    if data_[3] not in test_days:
                        test_days.append(data_[3])
                elif data_[3] == d1:
                    break

        print(test_days)
        print('test_days')
        return test_days

    def separate(self):
        data_all = self.data_all
        train = []
        test = []
        org_test = []
        # print('data_all')
        # print(data_all)
        # print(data_all.shape[1]) => 32
        # print(data_all.head())
        # print(data_all[0]['Tarih'])
        # print(list(data_all[len(data_all) - 1].values()))
        # print(len(list(data_all[0].values())))
        print(len(list(data_all[len(data_all) - 1].values())))

        for rows in range(len(data_all)):
            list_rows = []
            index = 0
            flag = 0
            count = 0
            data_all_ = list(data_all[rows].values())
            for cols in range(9, len(data_all_)):
                taken = 0
                # print(cols)
                if len(data_all_) == 32:
                    if data_all[rows]['Tarih'] not in self.test_days:
                        if data_all[rows]['IY'] != '' and data_all[rows]['MS'] != '':
                            if str(data_all_[cols]) == '-' or str(data_all_[cols]) == 'nan' or str(data_all_[cols]) == '#SAYI/0!' or \
                                    str(data_all_[cols]) == '#DEĞER!' or \
                                    str(data_all_[cols]) == 'ERT.' or str(data_all_[cols]) == 'ERT':
                                if taken == 0:
                                    list_rows.insert(index, '0,0')
                                    index += 1
                                    taken += 1
                            elif not data_all_[cols]:
                                count += 1
                            else:
                                if "," in data_all_[cols]:
                                    if taken == 0:
                                        list_rows.insert(index, float(data_all_[cols].replace(",", ".")))
                                        index += 1
                                        taken += 1
                                elif str(data_all_[cols]) != '':
                                    if taken == 0:
                                        list_rows.insert(index, float(data_all_[cols]))
                                        index += 1
                                        taken += 1
                            flag = 1

                    if data_all[rows]['Tarih'] in self.test_days or data_all[rows]['Tarih'] == d1:
                        if (data_all[rows]['IY'] == 'v' or data_all[rows]['IY'] == '-') and \
                                (data_all[rows]['MS'] == 'v' or data_all[rows]['MS'] == '-'):
                            if str(data_all_[cols]) == '-' or str(data_all_[cols]) == 'nan' or \
                                    str(data_all_[cols]) == '#SAYI/0!' or str(data_all_[cols]) == '#DEĞER!' or \
                                    str(data_all_[cols]) == 'ERT.' or str(data_all_[cols]) == 'ERT' \
                                    or str(data_all_[cols]) == 'Yrdk.':
                                if taken == 0:
                                    list_rows.insert(index, '0,0')
                                    index += 1
                                    taken += 1

                            elif not data_all_[cols]:
                                count += 1

                            else:
                                if "," in data_all_[cols]:
                                    if taken == 0:
                                        list_rows.insert(index, float(data_all_[cols].replace(",", ".")))
                                        index += 1
                                        taken += 1

                                elif str(data_all_[cols]) != '':
                                    if taken == 0:
                                        list_rows.insert(index, float(data_all_[cols]))
                                        index += 1
                                        taken += 1

                            flag = 2

            if flag == 1:
                if count == 0:
                    value = self.filter('MS15U', str(data_all_[7]), str(data_all_[8]))
                    if value != 2:
                        list_rows.insert(index, value)
                        index += 1
                        train.append(list_rows)
            elif flag == 2:
                if count == 0:
                    list_rows.insert(index, 0)
                    index += 1
                    # print(data_all_[3], data_all_[4])
                    # print(data_all_)
                    # print(list_rows)
                    test.append(list_rows)
                    first_part = []
                    ix = 0
                    for inc in range(0, 9):
                        first_part.insert(ix, data_all_[inc])
                        ix += 1
                    for inc_ in range(len(list_rows)):
                        first_part.insert(ix, list_rows[inc_])
                        ix += 1
                    org_test.append(first_part)

        train_ = pd.DataFrame(data=train, copy=True)
        test_ = pd.DataFrame(data=test, copy=True)
        org_test_ = pd.DataFrame(data=org_test, copy=True)
        # print(org_test_)
        # print(train_.shape[0])

        return train_, test_, org_test_

    @staticmethod
    def filter(fit, iy, ms):
        value_iy = iy.strip().split('-')
        value_ms = ms.strip().split('-')
        flag_iy = 0
        flag_ms = 0

        if len(value_iy) == 2:
            if value_iy[0].strip() != '' and value_iy[0].strip() != '':
                sum_iy = int(value_iy[0].strip()) + int(value_iy[1].strip())
                flag_iy = 1
        if len(value_ms) == 2:
            if value_ms[0].strip() != '' and value_ms[0].strip() != '':
                sum_ms = int(value_ms[0].strip()) + int(value_ms[1].strip())
                flag_ms = 1
            # else:
                # print(value_ms)

        if fit == 'MS15U':
            if flag_ms == 1:
                if sum_ms > 1:
                    return 1
                else:
                    return 0
            else:
                return 2
        elif fit == 'IY15U':
            if flag_iy == 1:
                if sum_iy > 1:
                    return 1
                else:
                    return 0
            else:
                return 2


class ML:
    def __init__(self, train, test, org_test):
        self.train = train
        self.test = test
        self.org_test = org_test
        self.features = []
        self.target = []
        self.models = []
        self.data_all = []

    def main(self):
        print('ML main started')
        data_all = database.main2()
        self.data_all = data_all
        features, target, features_test, target_test = self.drop_columns()
        self.target = target
        self.features = features
        train_x, test_x, y_train, y_test = self.feature_scaling()
        self.models = self.method_call()
        self.models_train(train_x, test_x, y_train, y_test)

        if len(features_test) > 0:
            all_predicts = self.model_test(features_test, target_test)
            # self.find_org_all()
            self.check_insert_db(all_predicts)

    def drop_columns(self):
        filtered_data = self.train
        features = filtered_data.drop('filter', axis=1)  # data
        # features = features.drop(drop_col, axis=1)
        target = filtered_data['filter']  # target
        features_test = []
        target_test = []
        if len(self.test) > 0:
            filtered_test = self.test
            features_test = filtered_test.drop('filter', axis=1)  # data
            # features_test = features_test.drop(drop_col, axis=1)
            target_test = filtered_test['filter']  # target

        return features, target, features_test, target_test

    def feature_scaling(self):

        features_ = self.features
        scaled_values = MinMaxScaler().fit_transform(features_)
        features_.loc[:, :] = scaled_values

        self.features = features_

        train_x, test_x, y_train, y_test = train_test_split(self.features,  self.target, stratify=self.target,
                                                            test_size=0.02, random_state=42)
        return train_x, test_x, y_train, y_test

    def models_train(self, train_x, test_x, y_train, y_test):
        for name, model in self.models:
            clf = model

            clf.fit(train_x, y_train)
            prediction_y = clf.predict(test_x)
            predict_score = int(precision_score(y_test, prediction_y)*100)
            # print(name)
            # print(predict_score)

    def model_test(self, features_test, target_test):
        # print(features_test.loc[10])
        # print(self.org_test.loc[10])
        all_predicts = []
        for name, model in self.models:
            clf = model

            clf.fit(self.features, self.target)

            prediction_y = clf.predict(features_test)
            # print(prediction_y)
            dict_ = {'model': name, 'precs': list(prediction_y)}
            all_predicts.append(dict_)

            # prec_score = int(precision_score(target_test, prediction_y) * 100)
            # print(prec_score)
        # print(all_predicts)
        # for ix in range(len(all_predicts)):
        #     print(all_predicts[ix])
        return all_predicts

    def find_org_all(self):

        print(list(self.org_test.columns))
        for inx in range(len(self.org_test)):
            print(self.org_test.loc[inx])
            for iny in list(self.org_test.columns):
                print(self.org_test.loc[inx][iny])

    def check_insert_db(self, all_predicts):

        data = self.data_all
        # print('all_predicts')
        # print(all_predicts)
        # print(self.org_test.loc[0])
        # print(data)
        bound_up = len(data) - 1
        eliminated = []

        org_ = self.org_test
        if bound_up > 0:
            for rows in (range(bound_up, -1, -1)):
                data_ = list(data[rows].values())
                # print(data_[3])

                for inx in range(len(org_)):
                    if str(org_.loc[inx]['Hafta']) == str(data_[1]):
                        if str(org_.loc[inx]['Tarih']) == str(data_[3]):
                            if str(org_.loc[inx]['Lig']) == str(data_[4]):
                                if str(org_.loc[inx]['EvSahibi']) == str(data_[5]):
                                    if str(org_.loc[inx]['Misafir']) == str(data_[6]):
                                        eliminated.append(inx)
                                        break
            # Adding on DB
            for inx in range(len(org_)):
                if inx not in eliminated:
                    data_ = {"Hafta": str(org_.loc[inx]['Hafta']), "Gun": org_.loc[inx]['Gun'],
                             "Tarih": str(org_.loc[inx]['Tarih']),
                             "Lig": org_.loc[inx]['Lig'], "EvSahibi": org_.loc[inx]['EvSahibi'],
                             "Misafir": str(org_.loc[inx]['Misafir']),
                             "MS1": str(org_.loc[inx]['MS1']), "MSX": str(org_.loc[inx]['MSX']),
                             "MS2": str(org_.loc[inx]['MS2']),
                             "IY1": str(org_.loc[inx]['IY1']),  "IYX": str(org_.loc[inx]['IYX']),
                             "IY2": str(org_.loc[inx]['IY2']),
                             "KGVar": str(org_.loc[inx]['KGVar']), "KGYok": str(org_.loc[inx]['KGYok']), "birX": str(org_.loc[inx]['birX']),
                             "bir2": str(org_.loc[inx]['bir2']), "x2": str(org_.loc[inx]['x2']), "iy15a": str(org_.loc[inx]['iy15a']),
                             "iy15u": str(org_.loc[inx]['iy15u']), "au15a": str(org_.loc[inx]['au15a']), "au15u": str(org_.loc[inx]['au15u']),
                             "au25a": str(org_.loc[inx]['au25a']), "au25u": str(org_.loc[inx]['au25u']), "au35a": str(org_.loc[inx]['au35a']),
                             "au35u": str(org_.loc[inx]['au35u']), "sifir1": str(org_.loc[inx]['sifir1']), "iki3": str(org_.loc[inx]['iki3']),
                             "dort6": str(org_.loc[inx]['dort6']), "yediplus": str(org_.loc[inx]['yediplus']),
                             "ModelLR": str(all_predicts[0]['precs'][inx]), "ModelLDA": str(all_predicts[1]['precs'][inx]),
                             "ModelKMeans": str(all_predicts[2]['precs'][inx])}
                    # print(data_)
                    database.insert_data(data_, "Prediction")

    @staticmethod
    def method_call():
        models = [("LR", LogisticRegression()), ('LDA', LinearDiscriminantAnalysis()),
                  ("K-Means", KMeans(n_clusters=2))]

        return models


def main():
    while True:
        fix = Fix()
        fix.main()
        # print('Fix test')
        # print(fix.test.values[0])
        ml = ML(fix.train, fix.test, fix.org_test)
        ml.main()


if __name__ == '__main__':
    main()
