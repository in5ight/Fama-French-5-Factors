import pandas as pd


def main():
    # 导入月个股回报
    stockmnth0 = pd.read_excel('./ff5f_data/stockmnth/TRD_Mnth0.xlsx')
    stockmnth1 = pd.read_excel('./ff5f_data/stockmnth/TRD_Mnth1.xlsx')
    stockmnth2 = pd.read_excel('./ff5f_data/stockmnth/TRD_Mnth2.xlsx')
    stockmnth = pd.concat([stockmnth0, stockmnth1, stockmnth2])
    stockmnth = stockmnth[(stockmnth['Markettype'] == 1) |
                          (stockmnth['Markettype'] == 4)]
    stockmnth = stockmnth[['Stkcd', 'Trdmnt', 'Msmvosd', 'Mretwd']]

    # 导入综合月市场回报
    mktmnth0 = pd.read_excel('./ff5f_data/mktmnth/TRD_Cnmont.xlsx')
    mktmnth1 = pd.read_excel('./ff5f_data/mktmnth/TRD_Cnmont1.xlsx')
    mktmnth = pd.concat([mktmnth0, mktmnth1])
    mktmnth = mktmnth[mktmnth['Markettype'] == 5]
    mktmnth = mktmnth[['Trdmnt', 'Cmretwdos']]

    # 导入无风险利率
    rf = pd.read_excel('./ff5f_data/rf/TRD_Nrrate.xlsx')[['Clsdt', 'Nrrmtdt']]
    # 取月末的值

    def month(x):
        return x[0:7]

    rf['Trdmnt'] = rf['Clsdt'].apply(month)
    rf = rf.sort_values(by=['Clsdt'])
    rf = rf.drop_duplicates(subset=['Trdmnt'], keep='last')
    rf = rf[['Trdmnt', 'Nrrmtdt']]

    # 合并三张表
    mkt = pd.merge(stockmnth, mktmnth, on=['Trdmnt'])
    mkt = pd.merge(mkt, rf, on=['Trdmnt'])
    mkt = mkt.dropna()
    mkt.to_csv('./data/mkt.csv', index=False)


if __name__ == '__main__':
    main()
