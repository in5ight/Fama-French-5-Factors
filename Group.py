import pandas as pd
import numpy as np


# 下面四个函数用于标记每个股票所属的组
def Size_group(x, split):
    if x <= split:
        return 'S'
    else:
        return 'B'


def BM_group(x, split_1, split_2):
    if x <= split_1:
        return 'L'
    elif split_1 < x <= split_2:
        return 'N'
    else:
        return 'H'


def OP_group(x, split_1, split_2):
    if x <= split_1:
        return 'W'
    elif split_1 < x <= split_2:
        return 'N'
    else:
        return 'R'


def INV_group(x, split_1, split_2):
    if x <= split_1:
        return 'C'
    elif split_1 < x <= split_2:
        return 'N'
    else:
        return 'A'


# 将分组结果保存到本地，无返回值
def save_group(t):
    # t为年份，输入类型为字符串，如'2016'

    data = pd.read_csv('./data/' + t + '期的指标.csv')

    # 对每个股票所属的组进行标记
    data['Size_group'] = data['Size'].apply(
        Size_group, args=[np.percentile(data['Size'], 50)])
    data['BM_group'] = data['BM'].apply(
        BM_group, args=[np.percentile(data['BM'], 30), np.percentile(data['BM'], 70)])
    data['OP_group'] = data['OP'].apply(
        OP_group, args=[np.percentile(data['OP'], 30), np.percentile(data['OP'], 70)])
    data['INV_group'] = data['INV'].apply(
        INV_group, args=[np.percentile(data['INV'], 30), np.percentile(data['INV'], 70)])

    # 保存到文件
    data[(data['Size_group'] == 'S') & (
        data['BM_group'] == 'L')]['Stkcd'].to_csv('./group/' + t + 'BM_SL.csv', index=False)
    data[(data['Size_group'] == 'S') & (
        data['BM_group'] == 'N')]['Stkcd'].to_csv('./group/' + t + 'BM_SN.csv', index=False)
    data[(data['Size_group'] == 'S') & (
        data['BM_group'] == 'H')]['Stkcd'].to_csv('./group/' + t + 'BM_SH.csv', index=False)
    data[(data['Size_group'] == 'B') & (
        data['BM_group'] == 'L')]['Stkcd'].to_csv('./group/' + t + 'BM_BL.csv', index=False)
    data[(data['Size_group'] == 'B') & (
        data['BM_group'] == 'N')]['Stkcd'].to_csv('./group/' + t + 'BM_BN.csv', index=False)
    data[(data['Size_group'] == 'B') & (
        data['BM_group'] == 'H')]['Stkcd'].to_csv('./group/' + t + 'BM_BH.csv', index=False)

    data[(data['Size_group'] == 'S') & (
        data['OP_group'] == 'R')]['Stkcd'].to_csv('./group/' + t + 'OP_SR.csv', index=False)
    data[(data['Size_group'] == 'S') & (
        data['OP_group'] == 'N')]['Stkcd'].to_csv('./group/' + t + 'OP_SN.csv', index=False)
    data[(data['Size_group'] == 'S') & (
        data['OP_group'] == 'W')]['Stkcd'].to_csv('./group/' + t + 'OP_SW.csv', index=False)
    data[(data['Size_group'] == 'B') & (
        data['OP_group'] == 'R')]['Stkcd'].to_csv('./group/' + t + 'OP_BR.csv', index=False)
    data[(data['Size_group'] == 'B') & (
        data['OP_group'] == 'N')]['Stkcd'].to_csv('./group/' + t + 'OP_BN.csv', index=False)
    data[(data['Size_group'] == 'B') & (
        data['OP_group'] == 'W')]['Stkcd'].to_csv('./group/' + t + 'OP_BW.csv', index=False)

    data[(data['Size_group'] == 'S') & (
        data['INV_group'] == 'C')]['Stkcd'].to_csv('./group/' + t + 'INV_SC.csv', index=False)
    data[(data['Size_group'] == 'S') & (
        data['INV_group'] == 'N')]['Stkcd'].to_csv('./group/' + t + 'INV_SN.csv', index=False)
    data[(data['Size_group'] == 'S') & (
        data['INV_group'] == 'A')]['Stkcd'].to_csv('./group/' + t + 'INV_SA.csv', index=False)
    data[(data['Size_group'] == 'B') & (
        data['INV_group'] == 'C')]['Stkcd'].to_csv('./group/' + t + 'INV_BC.csv', index=False)
    data[(data['Size_group'] == 'B') & (
        data['INV_group'] == 'N')]['Stkcd'].to_csv('./group/' + t + 'INV_BN.csv', index=False)
    data[(data['Size_group'] == 'B') & (
        data['INV_group'] == 'A')]['Stkcd'].to_csv('./group/' + t + 'INV_BA.csv', index=False)


# 返回某个组的月收益，并保存到本地
def calc_return(group_file):
    group = pd.read_csv('./group/' + group_file)
    mkt = pd.read_csv('./data/mkt.csv')

    t = group_file[0:4]
    t1 = str(int(t) + 1)

    data = pd.merge(group, mkt, on=['Stkcd'])
    data = data[(data['Trdmnt'] == t+'-07') | (data['Trdmnt'] == t+'-08') | (data['Trdmnt'] == t+'-09')
                | (data['Trdmnt'] == t+'-10') | (data['Trdmnt'] == t+'-11') | (data['Trdmnt'] == t+'-12')
                | (data['Trdmnt'] == t1+'-01') | (data['Trdmnt'] == t1+'-02') | (data['Trdmnt'] == t1+'-03')
                | (data['Trdmnt'] == t1+'-04') | (data['Trdmnt'] == t1+'-05') | (data['Trdmnt'] == t1+'-06')]

    def month_return(x):
        sum = x['Msmvosd'].sum()
        res = x['Mretwd'] * x['Msmvosd'] / sum
        return res.sum()

    tmp = data.groupby('Trdmnt').apply(month_return)
    res = pd.DataFrame(tmp, columns=['return']).reset_index()
    res.to_csv('./group_return/' +
               group_file[0:-4] + '_return.csv', index=False)
    return res


def main():
    calc_return('2017OP_SW.csv')


if __name__ == '__main__':
    main()
