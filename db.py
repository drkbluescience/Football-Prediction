import pymongo
import pandas as pd
import helper


class DB:
    def __init__(self):
        self.columns = []
        self.columns_long = []

    def main(self):
        table = self.get_table("Match")
        # self.update_data_all()
        data_all = self.select_data(table)
        # self.select_fitered(data_all)
        return data_all

    def main2(self):
        table = self.get_table("Prediction")
        data_all = self.select_predicts_db(table)
        return data_all

    @staticmethod
    def get_table(db_name):
        try:
            client = pymongo.MongoClient(
                helper.vals['mongo_client'])

            # db = client.list_database_names()
            dbs = client.list_database_names()
            # print(dbs)
            db = client[db_name]
            table = db["table"]
            return table
        except Exception as e:
            print(e)
            return

    def select_fitered(self, data_all):
        table = self.get_table("Match")
        data_list = []
        last = table.find_one()
        last_week = data_all[len(data_all) - 1]['Hafta']
        last_week_bef = last_week - 1
        print('last filtered')

        for x in table.find():
            if x['Hafta'] == last_week or x['Hafta'] == last_week_bef:
                data_list.append(x)

        print(data_list)

    def select_data(self, table):
        try:
            table = table
            data_list = []
            for x in table.find():
                data_list.append(x)

            # key list -->
            # '_id', 'Hafta', 'Gun', 'Tarih', 'Lig', 'EvSahibi', 'Misafir', 'IY', 'MS', 'MS1', 'MSX', 'MS2', 'IY1',
            # 'IYX', 'IY2', 'KGVar', 'KGYok', 'birX', 'bir2', 'x2', 'iy15a', 'iy15u', 'au15a', 'au15u', 'au25a',
            # 'au25u', 'au35a', 'au35u', 'sifir1','iki3', 'dort6', 'yediplus'
            print(table.find_one().keys())
            self.columns = list(table.find_one().keys())
            self.columns_long = list(table.find_one().keys())
            print(self.columns)
            self.columns.remove('_id')
            self.columns.remove('Hafta')
            self.columns.remove('Gun')
            self.columns.remove('Tarih')
            self.columns.remove('Lig')
            self.columns.remove('EvSahibi')
            self.columns.remove('Misafir')
            self.columns.remove('IY')
            self.columns.remove('MS')
            # columns list -->
            self.columns.append('filter')
            self.columns_long.append('filter')
            print(self.columns)
            # print(self.columns[0])
            print(len(self.columns))
            df = pd.DataFrame(data_list)
            return data_list

        except Exception as e:
            print(e)
            return

    @staticmethod
    def select_predicts_db(table):
        try:
            table = table
            data_list = []
            for x in table.find():
                data_list.append(x)
            return data_list
        except Exception as e:
            print(e)
            return

    def insert_data(self, data, db_name):
        try:
            table = self.get_table(db_name)

            data_ = helper.keys

            # print(db.list_collection_names())
            table.insert_one(data)
            # table.insert_many(data)
        except Exception as e:
            print(e)

    def update_data_all(self):
        try:
            table = self.get_table("Match")
            # table.update_data({'_id': old[ix][0]}, {"$set": {'IY': new[iy][5]}})

            # filter_value = {'appliance': 'fan'}
            # new_values = {"$set": {'quantity': 25}}

            table.update_many({'Hafta': 81, 'Tarih': '23.01.2022'}, {"$set": {'Hafta': 80}})
            # table.update_one(filter_value, new_values)
            print('Update all done')
        except Exception as e:
            print(e)

    def update_data(self, filter_value, new_values):
        try:
            table = self.get_table("Match")
            # table.update_data({'_id': old[ix][0]}, {"$set": {'IY': new[iy][5]}})

            # filter_value = {'appliance': 'fan'}
            # new_values = {"$set": {'quantity': 25}}

            table.update_one(filter_value, new_values)
            # print('Update done')
        except Exception as e:
            print(e)

    def delete_data(self):
        query = {"address": "Mountain 21"}
        try:
            table = self.get_table("Match")
            for i in range(69, 80):
                table.delete_many({"Hafta": i})

        except Exception as e:
            print(e)


def main():
    # DB().main()
    DB()


if __name__ == '__main__':
    main()
