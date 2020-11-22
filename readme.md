输入数据放在文件夹ff5f_data里，输出的数据在data里

运行mkt.py，得到的是data/mkt.csv

运行FS.py，得到的是data/FS.csv

在得到上述两个csv文件之后，才能运行Value.py，得到的是data/*期指标，年份在程序中指定

在得到上面的指标后，才能运行Group.py，save_group得到的是分组结果，保存在group文件夹内；
calc_return得到的是某个组合的月收益率，保存在group_return文件夹内

类似SMB_INV&CMA.py相关文件是计算因子的程序，结果对应保存在factor_SMB_INV&CMA文件夹下