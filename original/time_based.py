# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 14:04:40 2019

@author: craig
"""

print("歡迎使用時間調整程式!"
      "這個程式可以由小間距的時間轉成大間距的時間\n"
      "若想要大間距轉小間距可以用其他程式\n"
      "以原資料幾秒一筆來看(需輸入資料)\n"
      "可以轉成時資料及日資料\n"
      "可以修改option參數，設定為hour_based(3600)、day_based(86400)或自定義秒數\n"
      "資料格式要求: 第一行為時間, 要有title, 存檔名稱須加上副檔名\n"
      "檔案會存於當前程式所在路徑!\n"
      "method可以調整為三種模式: 後減前、直接取值、加權平均\n"
      "\nAuthur: Cheng-Chung-Chiu & Lance Wan\n"
      "Contact: craigchiu0619@gmail.com")

import numpy as np
import os
import pandas as pd

class change_time():
    def __init__(self, 檔案路徑, 檔案名稱, 檔案格式, 開始時間 = 0, 結束時間 = -1,  original_time_based = 1, method = '直接取值', 存檔名稱 = '未命名檔案.xlsx', 存檔格式 = 'excel'):
        print('運作中，請稍後...')
        try:
            if 檔案格式 == 'csv':
                os.chdir(檔案路徑)
                self.file = pd.read_csv(檔案名稱, low_memory=False)
            else:
                os.chdir(檔案路徑)
                self.file = pd.read_excel(檔案名稱, low_memory=False)
        except:
            print('檔案路徑或名稱或副檔名有錯!')
        self.target = self.file.iloc[開始時間:結束時間]
        self.column = 0
        self.row = 0
        self.title = self.file.columns.tolist()
        self.time = []
        self.original_time_based = original_time_based
        self.method = method
        self.save_name = 存檔名稱
        self.save_file_type = 存檔格式
        
    def save(self, new_file):
        new_file = np.array(new_file, dtype = np.object)
        self.time = np.array(self.time, dtype = np.object)
        new_file = np.hstack((self.time.reshape(-1,1), new_file))
        new_file = np.vstack((self.title, new_file))
        file_dataframe = pd.DataFrame(new_file)
        if self.save_file_type == 'csv':
            file_dataframe.to_csv(self.save_name, index = False, header = None, sep=',')
            print("Done!")
            return
        file_dataframe.to_excel(self.save_name, index = False, header = None)
        print("Done!")
        
    def time_based(self, option = 'hour_based'):
        if option == 'hour_based':
            換算基礎 = int(3600 / self.original_time_based)
        if option == 'day_based':
            換算基礎 = int(86400 / self.original_time_based)
        if type(option) == int:
            換算基礎 = int(option / self.original_time_based)
            
        if 換算基礎 < 1:
            print("並非由小間距轉大間距!")
            return
        new_file = np.zeros((int(np.shape(self.target)[0] / 換算基礎), np.shape(self.target)[1]-1))
        row = 0
        column = 0

        for self.row in range(0, np.shape(self.target)[0] - 換算基礎, 換算基礎):
            self.time = np.append(self.time, self.target.iloc[self.row, 0])
        self.row = 0

        try:
            if self.method == '後減前':
                for self.column in range(1, np.shape(self.target)[1]):
                    for self.row in range(0, np.shape(self.target)[0] - 換算基礎, 換算基礎):
                        new_file[row, column] = self.target.iloc[self.row + 換算基礎, self.column] - self.target.iloc[self.row, self.column]
                        row += 1
                    row = 0
                    column += 1
            
            if self.method == '直接取值':
                for self.column in range(1, np.shape(self.target)[1]):
                    for self.row in range(0, np.shape(self.target)[0] - 換算基礎, 換算基礎):
                        new_file[row, column] = self.target.iloc[self.row, self.column]
                        row += 1
                    row = 0
                    column += 1
                
            if self.method == '加權平均':
                for self.row in range(0, np.shape(self.target)[0] - 換算基礎, 換算基礎):
                    new_file[row, :] = np.mean(self.target.iloc[self.row:self.row+換算基礎, 1:], 0)
                    row += 1
            
            change_time.save(self, new_file)
            
        except:
            print('不符合規則(可能為 1.資料格式有誤， 2.檔案存取被拒(須關閉檔案))')
            
            
檔案路徑 = 'C:\\Users\\craig\\OneDrive\\桌面\\高雄抽水水位(宇文)\\新增資料夾 (4)'
檔案名稱 = 'pdata.csv'
檔案格式 = 'csv'
開始時間 = 0 #第幾格開始轉
結束時間 = -1 #轉到第幾格結束(-1是最後一格)
original_time_based = 600 #幾秒一筆
method = '直接取值'
存檔名稱 = 'Test.xlsx'
存檔格式 = 'excel'
option = 'day_based'
            
s = change_time(檔案路徑, 檔案名稱, 檔案格式, 開始時間, 結束時間, original_time_based, method, 存檔名稱, 存檔格式)
s.time_based(option)
        