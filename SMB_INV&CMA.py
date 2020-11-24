# _*_ coding:utf-8 _*_
# 开发人员:Stephen
# 开发时间：2020/11/22 9:37
# 文件名：SMB_INV&CMA.py
# 开发工具：PyCharm

import pandas as pd
import os

def SMB_INV(t):
    # 读取数据，对应相应路径
    SC = pd.read_csv('./group_return/' + t + 'INV_SC_return.csv')
    SN = pd.read_csv('./group_return/' + t + 'INV_SN_return.csv')
    SA = pd.read_csv('./group_return/' + t + 'INV_SA_return.csv')
    BC = pd.read_csv('./group_return/' + t + 'INV_BC_return.csv')
    BN = pd.read_csv('./group_return/' + t + 'INV_BN_return.csv')
    BA = pd.read_csv('./group_return/' + t + 'INV_BA_return.csv')

    #计算指标
    tmp = (SC['return'] + SN['return'] + SA['return'] - BC['return'] -
           BN['return'] + BA ['return']) / 3
    #日期
    res = pd.concat([SC['Trdmnt'], tmp], axis=1)
    res.columns = ['Trdmnt', 'SMB_INV']
    #保存数据
    File_Path = os.getcwd() + '\\factor_SMB_INV&CMA\\'
    # 获取到当前文件的目录，并检查是否有相应文件夹，如果不存在则自动新建文件夹
    if not os.path.exists(File_Path):
        os.makedirs(File_Path)
    res.to_csv('./factor_SMB_INV&CMA/' + t + 'SMB_inv.csv', index=False)

    return res


def CMA(t):
    SC = pd.read_csv('./group_return/' + t + 'INV_SC_return.csv')
    SA = pd.read_csv('./group_return/' + t + 'INV_SA_return.csv')
    BC = pd.read_csv('./group_return/' + t + 'INV_BC_return.csv')
    BA = pd.read_csv('./group_return/' + t + 'INV_BA_return.csv')

    tmp = (SC['return'] + BC['return'] - SA['return'] - BA['return']) / 2

    res = pd.concat([SC['Trdmnt'], tmp], axis=1)
    res.columns = ['Trdmnt', 'RMW']

    File_Path = os.getcwd() + '\\factor_SMB_INV&CMA\\'
    # 获取到当前文件的目录，并检查是否有相应文件夹，如果不存在则自动新建文件夹
    if not os.path.exists(File_Path):
        os.makedirs(File_Path)
    res.to_csv('./factor_SMB_INV&CMA/' + t + 'CMA.csv', index=False)
    return res


def main():
    SMB_INV('2016')
    SMB_INV('2017')

    CMA('2016')
    CMA('2017')


if __name__ == '__main__':
    main()