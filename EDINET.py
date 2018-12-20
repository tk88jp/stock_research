# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 13:21:57 2018

@author: kaseda
"""

from edinet_xbrl.edinet_xbrl_downloader import EdinetXbrlDownloader
from edinet_xbrl.edinet_xbrl_parser import EdinetXbrlParser
import os
import time
import glob
import pandas as pd
import numpy as np


data_dir = os.path.dirname(os.path.abspath(__file__))

#XBRLをダウンロード
def xbrl_downloader(ticker):

    ## set a ticker you want to download xbrl file
    ticker = ticker    
    
    target_dir = data_dir + '/xbrl'
    
    ## init downloader
    xbrl_downloader = EdinetXbrlDownloader()
    
    #フォルダ作成
    os.chdir(target_dir)
    try:
        os.mkdir(ticker)
    except FileExistsError:
        pass
    
    #保存フォルダに移動
    save_dir = target_dir + '/' + ticker
    
    #ファイル
    xbrl_downloader.download_by_ticker(ticker, save_dir)


def value_pickup(ticker):

    ticker = ticker     
    target_dir = data_dir + '/xbrl/' + ticker

    #欲しいファイルを見つける
    os.chdir(target_dir)
    filelist = glob.glob('./*')
    #print(filelist)
    daylist = []
    for a in range(len(filelist)):
        new_day = filelist[a][(len(filelist[a])-15) : (len(filelist[a])-5)]
        daylist.append(new_day)
    max_index = daylist.index(min(daylist))
    print(daylist)
    print(max_index)
    print(filelist[1][2:])
    
    ## init parser
    parser = EdinetXbrlParser()
    
    ## parse xbrl file and get data container
    xbrl_file_path = target_dir
    edinet_xbrl_object = parser.parse_file(xbrl_file_path+'/'+filelist[1][2:])
    
    ## 例えば、該当年度の総資産を取ってみる
    key = "jppfs_cor:Assets"
    context_ref = "Prior1YearInstant"#CurrentYearInstant
    current_year_assets = edinet_xbrl_object.get_data_by_context_ref(key, context_ref).get_value()
    
    current_year_assets = np.array([int(current_year_assets)])
    
    #保存
    output_dir = data_dir + '/output'
    os.chdir(output_dir)
    try:
        os.mkdir(ticker)
    except FileExistsError:
        pass    
    os.chdir(output_dir + '/' + ticker)    
    
    np.savetxt(ticker+'.txt', current_year_assets)
    
    return current_year_assets



if __name__ == '__main__':
    start = time.time()
    ticker = str(7523)
    #xbrl_downloader(ticker)
    print(value_pickup(ticker))
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
