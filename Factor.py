import pandas as pd


class Factor:
    def __init__(self, year):
        # year为年份，字符串形式
        self.fs = pd.read_csv('./data/FS.csv')
        self.mkt = pd.read_csv('./data/mkt.csv')
        self.t = year

    def Size(self):
        date = self.t + '-06'
        df = self.mkt[self.mkt['Trdmnt'] == date]
        df['Size'] = df['Msmvosd']
        # 输出的结果按市值从小到大排序
        df = df.sort_values(by=['Size'])
        return df

    def BM(self):
        date = str(int(self.t) - 1) + '-12'
        df_mkt = self.mkt[self.mkt['Trdmnt'] == date]
        df_fs = self.fs[self.fs['Accper'] == date + '-31']

        # 日期统一格式
        def month(x):
            return x[0:7]
        df_fs['Trdmnt'] = df_fs['Accper'].apply(month)

        df = pd.merge(df_mkt, df_fs, on=['Stkcd', 'Trdmnt'])
        df['BM'] = df['total_equity'] / df['Msmvosd']
        df = df.sort_values(by=['BM'])
        return df

    def OP(self):
        date = str(int(self.t) - 1) + '-12'
        df_fs = self.fs[self.fs['Accper'] == date + '-31']

        # 日期统一格式
        def month(x):
            return x[0:7]
        df_fs['Trdmnt'] = df_fs['Accper'].apply(month)
        df_fs['OP'] = df_fs['operating profit'] / df_fs['total_equity']
        df_fs = df_fs.sort_values(by=['OP'])
        return df_fs

    def INV(self):
        date1 = str(int(self.t) - 1) + '-12'
        date2 = str(int(self.t) - 2) + '-12'
        df_fs = self.fs[(self.fs['Accper'] == date1 + '-31') |
                        (self.fs['Accper'] == date2 + '-31')]

        # 日期统一格式
        def month(x):
            return x[0:7]
        df_fs['Trdmnt'] = df_fs['Accper'].apply(month)

        df_fs['last_total'] = df_fs['total_assets'].shift()
        df_fs['up_id'] = df_fs['Stkcd'].shift()
        df_fs = df_fs[df_fs['Stkcd'] == df_fs['up_id']]
        df_fs['INV'] = (df_fs['total_assets'] -
                        df_fs['last_total']) / df_fs['last_total']
        df_fs = df_fs.drop(columns=['last_total', 'up_id'])
        df_fs = df_fs.sort_values(by=['INV'])
        return df_fs

    def output(self):
        Size = self.Size()[['Stkcd', 'Size']]
        BM = self.BM()[['Stkcd', 'BM']]
        OP = self.OP()[['Stkcd', 'OP']]
        INV = self.INV()[['Stkcd', 'INV']]

        df_factor = pd.merge(Size, BM, on=['Stkcd'])
        df_factor = pd.merge(df_factor, OP, on=['Stkcd'])
        df_factor = pd.merge(df_factor, INV, on=['Stkcd'])
        df_factor['t'] = self.t
        df_factor = df_factor.sort_values(by=['Stkcd'])
        df_factor.to_csv('./data/' + self.t + '期的指标.csv', index=False)
        return df_factor


def main():
    factor = Factor('2017')
    print(factor.output())


if __name__ == '__main__':
    main()
