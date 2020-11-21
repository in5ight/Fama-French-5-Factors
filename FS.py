import pandas as pd


def main():
    # 导入资产负债表数据
    bs1 = pd.read_excel('./ff5f_data/Balance sheet/FS_Combas1.xlsx')
    bs2 = pd.read_excel('./ff5f_data/Balance sheet/FS_Combas2.xlsx')
    bs3 = pd.read_excel('./ff5f_data/Balance sheet/FS_Combas3.xlsx')
    bs = pd.concat([bs1, bs2, bs3], ignore_index=True)
    bs = bs[['Stkcd', 'Accper', 'Typrep', 'total_assets',
             'tptal_liability', 'total_equity']]
    bs = bs[bs['Typrep'] == 'A']

    # 导入利润表数据
    is1 = pd.read_excel('./ff5f_data/Income statement/FS_Comins1.xlsx')
    is2 = pd.read_excel('./ff5f_data/Income statement/FS_Comins2.xlsx')
    is3 = pd.read_excel('./ff5f_data/Income statement/FS_Comins3.xlsx')
    is0 = pd.concat([is1, is2, is3], ignore_index=True)
    is0 = is0[['Stkcd', 'Accper', 'Typrep', 'operating profit']]
    is0 = is0[is0['Typrep'] == 'A']

    # 将资产负债表和利润表合并
    fs = pd.merge(bs, is0, on=['Stkcd', 'Accper', 'Typrep'])

    # 只保留6月和12月的数据
    def judge_6or12(x):
        if x[5:7] == '06' or x[5:7] == '12':
            return 1
        else:
            return 0
    fs['judge'] = fs['Accper'].apply(judge_6or12)
    fs = fs[fs['judge'] == 1]
    fs = fs.drop(['judge'], axis=1)
    fs = fs.dropna()
    fs = fs.sort_values(by=['Stkcd', 'Accper'])
    fs.to_csv('./data/FS.csv', index=False)


if __name__ == '__main__':
    main()
