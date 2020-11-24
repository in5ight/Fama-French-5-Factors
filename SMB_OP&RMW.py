# -*- coding: utf-8 -*-


import pandas as pd


def SMB_OP(t):
    

    SR = pd.read_csv('./group_return/' + t +'OP_SR_return.csv')
    SN = pd.read_csv('./group_return/' + t +'OP_SN_return.csv')
    SW = pd.read_csv('./group_return/' + t +'OP_SW_return.csv')
    BR = pd.read_csv('./group_return/' + t +'OP_BR_return.csv')
    BN = pd.read_csv('./group_return/' + t +'OP_BN_return.csv')
    BW = pd.read_csv('./group_return/' + t +'OP_BW_return.csv')
   
    tmp=(SR['return']+SN['return']+SW['return']-BR['return']-
        BN['return']+BW['return'])/3

    res = pd.concat([SR['Trdmnt'],tmp],axis=1)
    res.columns = ['Trdmnt','SMB_OP']
    
    res.to_csv('./factor/'+t+'SMB_OP.csv', index=False)
    #首次运行需要在根目录下创建factor文件夹
    return res
    
def  RMW(t):
    SR = pd.read_csv('./group_return/' + t +'OP_SR_return.csv')
    BR = pd.read_csv('./group_return/' + t +'OP_BR_return.csv')
    SW = pd.read_csv('./group_return/' + t +'OP_SW_return.csv')
    BW = pd.read_csv('./group_return/' + t +'OP_BW_return.csv')
    
    tmp=(SR['return']+BR['return']-SW['return']-BW['return'])/2

    res = pd.concat([SR['Trdmnt'],tmp],axis=1)
    res.columns = ['Trdmnt','RMW']
    
    res.to_csv('./factor/'+t+'RMW.csv', index=False)
    return res
def main():
    SMB_OP('2016')
    SMB_OP('2017')
    
    RMW('2016')
    RMW('2017')
if __name__ == '__main__':
    main()