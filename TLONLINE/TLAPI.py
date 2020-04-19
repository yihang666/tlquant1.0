import tushare as ts
from jqdatasdk import *
auth("15336553896","553896")
import  pandas as pd
import time
import matplotlib.pyplot as plt
import datetime
token = '624f1a291a6d3bec690c866a2ef0c4cc3876e11743ae207221bfed19'
ts.set_token(token)

pro = ts.pro_api()
def LastTradeDay():
    dfDate = pro.trade_cal(start_date=beforeDate, end_date=nowDate,pretrade_date = True)
    for i in range(len(dfDate.index)-2,-1,-1):
        if dfDate.iloc[i,2]==1:
            result = dfDate.iloc[i,1]
            break
    return  result

#日期与实践模块

nowTime = datetime.datetime.now()
beforeTime = nowTime - datetime.timedelta(days=29)
beforeHalfYearTime = nowTime -datetime.timedelta(days=180)
yesterdayTime =  nowTime - datetime.timedelta(days=1)

#给tushare喂的数据
nowDate = nowTime.date().strftime("%Y%m%d")
beforeDate = beforeTime.date().strftime("%Y%m%d")
beforeHalfYearDate = beforeHalfYearTime.date().strftime("%Y%m%d")
yesterdayDate = yesterdayTime.date().strftime("%Y%m%d")


#给聚宽喂的数据
nowDateJQ = nowTime.date().strftime("%Y-%m-%d")
beforeDateJQ = beforeTime.date().strftime("%Y-%m-%d")
beforeHalfYearDateJQ = beforeHalfYearTime.date().strftime("%Y-%m-%d")
yesterdayDateJQ = yesterdayTime.date().strftime("%Y-%m-%d")

#上一交易日
lastTradeDate = LastTradeDay()
lastTradeTime = datetime.datetime.strptime(lastTradeDate, "%Y%m%d")
lastTradeDateJQ = lastTradeTime.date().strftime("%Y-%m-%d")





def Current():
    dfCurrent = pro.fx_daily(ts_code='USDCNH.FXCM', start_date=beforeHalfYearDate, end_date=nowDate)
    dfCurrent = dfCurrent[['trade_date', 'bid_open', 'bid_close']]
    CurrentImg = dfCurrent.plot(x= 'trade_date',title="USD CURRENCY")
    plt.sca(CurrentImg)
    CurrentImg = plt.gca().invert_xaxis()
    return CurrentImg

def WenzhouIndex():
    dfWenzhouIndex = pro.wz_index(start_date=beforeHalfYearDate, end_date=nowDate)
    dfMingJianZiBen = dfWenzhouIndex[['date', 'cm_rate']]
    MingJianZiBenImg = dfMingJianZiBen.plot(x='date', title="Private capital management company, direct financing price")
    return MingJianZiBenImg

def ConceptVolumeRank():
    allConcepts = get_concepts()
    for i in allConcepts.index:
        allConceptStocks = get_concept_stocks(i, date=nowDateJQ)
        try:
            panel = get_price(allConceptStocks, start_date=beforeDateJQ, end_date=nowDateJQ)
        except:
            print("i = %s" %i)
            continue
        dfVolume = panel['volume']
        dfVolume['SUM'] = dfVolume.apply(lambda x: x.sum(),axis = 1)
        nowVolume = dfVolume.loc[nowDateJQ, 'SUM']
        yesterdayVolume = dfVolume.loc[lastTradeDateJQ, 'SUM']
        volumeRatio = nowVolume / yesterdayVolume
        allConcepts.loc[i, 'volumeRatio'] = volumeRatio
    conceptVolumeRank = allConcepts.sort_values(by="volumeRatio", ascending=False).head(20)
    return conceptVolumeRank

def IndustryVolumeRank():
    allIndustry = get_industries(name='sw_l1', date=nowDateJQ)
    for i in allIndustry.index:
        allIndustryStocks = get_industry_stocks(i, date=nowDateJQ)
        try:
            panelIndustry = get_price(allIndustryStocks, start_date=beforeDateJQ, end_date=nowDateJQ,panel=True)
        except:
            print("i = %s" % i)
            continue
        dfIndustryVolume = panelIndustry['volume']
        dfIndustryVolume['SUM'] = dfIndustryVolume.apply(lambda x: x.sum(), 1)
        nowIndustryVolume = dfIndustryVolume.loc[nowDateJQ, 'SUM']
        yesterdayIndustryVolume = dfIndustryVolume.loc[lastTradeDateJQ, 'SUM']
        volumeRatio = nowIndustryVolume / yesterdayIndustryVolume
        allIndustry.loc[i, 'volumeRatio'] = volumeRatio
    industryVolumeRank = allIndustry.sort_values(by="volumeRatio", ascending=False).head(10)
    industryVolumeRank = industryVolumeRank[['name','volumeRatio']]
    industryVolumeRankImg = industryVolumeRank.plot(kind='bar',x='name',title = '每日行业板块放量')
    return industryVolumeRankImg

def IndustryVolumeRankSW_L2():
    allIndustry = get_industries(name='sw_l2', date=nowDateJQ)
    for i in allIndustry.index:
        allIndustryStocks = get_industry_stocks(i, date=nowDateJQ)
        try:
            panelIndustry = get_price(allIndustryStocks, start_date=beforeDateJQ, end_date=nowDateJQ)
        except:
            print("i = %s" % i)
            continue
        dfIndustryVolume = panelIndustry['volume']
        dfIndustryVolume['SUM'] = dfIndustryVolume.apply(lambda x: x.sum(), axis=1)
        nowIndustryVolume = dfIndustryVolume.loc[nowDateJQ, 'SUM']
        yesterdayIndustryVolume = dfIndustryVolume.loc[lastTradeDateJQ, 'SUM']
        volumeRatio = nowIndustryVolume / yesterdayIndustryVolume
        allIndustry.loc[i, 'volumeRatio'] = volumeRatio
    industryVolumeRank = allIndustry.sort_values(by="volumeRatio", ascending=False).head(10)
    industryVolumeRank = industryVolumeRank[['name','volumeRatio']]
    industryVolumeRankImg = industryVolumeRank.plot(kind='bar',x='name',title = '每日行业板块放量')
    return industryVolumeRankImg


def IndustryVolumeWeekRank():
    allIndustry = get_industries(name='sw_l1', date=nowDateJQ)
    for i in allIndustry.index:
        allIndustryStocks = get_industry_stocks(i, date=nowDateJQ)
        try:
            panelIndustry = get_price(allIndustryStocks, start_date=beforeDateJQ, end_date=nowDateJQ)
        except:
            print("i = %s" % i)
            continue
        dfIndustryVolume = panelIndustry['volume']
        dfIndustryVolume['SUM'] = dfIndustryVolume.apply(lambda x: x.sum(), axis=1)
        volumeThisWeek = dfIndustryVolume['SUM'].ix[-5:]
        volumeThisWeekNum = volumeThisWeek.sum()

        volumeLastWeek = dfIndustryVolume['SUM'].ix[-10:]
        volumeLastWeekNum = volumeLastWeek.sum()

        volumeWeekRatio = volumeThisWeekNum / (volumeLastWeekNum - volumeThisWeekNum)
        allIndustry.loc[i, 'volumeWeekRatio'] = volumeWeekRatio
    industryVolumeWeekRank = allIndustry.sort_values(by="volumeWeekRatio", ascending=False).head(10)
    industryVolumeWeekRank = industryVolumeWeekRank[['name', 'volumeWeekRatio']]
    industryVolumeWeekRankImg = industryVolumeWeekRank.plot(kind='bar', x='name',title = "五交易日行业板块放量（每日更新）")
    return industryVolumeWeekRankImg

def IndustryVolumeWeekRankSW_L2():
    allIndustry = get_industries(name='sw_l2', date=nowDateJQ)
    for i in allIndustry.index:
        allIndustryStocks = get_industry_stocks(i, date=nowDateJQ)
        try:
            panelIndustry = get_price(allIndustryStocks, start_date=beforeDateJQ, end_date=nowDateJQ)
        except:
            print("i = %s" % i)
            continue
        dfIndustryVolume = panelIndustry['volume']
        dfIndustryVolume['SUM'] = dfIndustryVolume.apply(lambda x: x.sum(), axis=1)
        volumeThisWeek = dfIndustryVolume['SUM'].ix[-5:]
        volumeThisWeekNum = volumeThisWeek.sum()

        volumeLastWeek = dfIndustryVolume['SUM'].ix[-10:]
        volumeLastWeekNum = volumeLastWeek.sum()

        volumeWeekRatio = volumeThisWeekNum / (volumeLastWeekNum - volumeThisWeekNum)
        allIndustry.loc[i, 'volumeWeekRatio'] = volumeWeekRatio
    industryVolumeWeekRank = allIndustry.sort_values(by="volumeWeekRatio", ascending=False).head(10)
    industryVolumeWeekRank = industryVolumeWeekRank[['name', 'volumeWeekRatio']]
    industryVolumeWeekRankImg = industryVolumeWeekRank.plot(kind='bar', x='name',title = "五交易日行业板块放量（每日更新）")
    return industryVolumeWeekRankImg

def NorthMoney():
    moneyFlow = pro.moneyflow_hsgt(start_date=beforeDate, end_date=nowDate)
    northMoneyFlow = moneyFlow[['trade_date', 'hgt', "sgt", "north_money"]]
    northMoneyFlow.rename(columns={'hgt':'沪股通','sgt':'深股通','north_money':'北向资金'}, inplace = True)
    imgNorthMoney = northMoneyFlow.plot(x="trade_date",title = "北向资金",kind = 'bar')
    plt.sca(imgNorthMoney)
    imgNorthMoney = plt.gca().invert_xaxis()
    return imgNorthMoney

def SouthMoney():
    moneyFlow = pro.moneyflow_hsgt(start_date=beforeDate, end_date=nowDate)
    southMoneyFlow = moneyFlow[['trade_date', 'ggt_ss', "ggt_sz", "south_money"]]
    imgSouthMoney = southMoneyFlow.plot(x="trade_date",title = "SouthMoney")
    return imgSouthMoney

def Shibor():
    dfShibor = pro.shibor(start_date=beforeDate, end_date=nowDate)
    dfShibor = dfShibor[['date','on','1w','2w']]
    imgShibor = dfShibor.plot(x='date', title='Shibor')
    plt.sca(imgShibor)
    imgShibor = plt.gca().invert_xaxis()
    return imgShibor

def TodayMacroData():
    dfTodayMacroData = pro.eco_cal(date=nowDate)
    return dfTodayMacroData


def Margin():
    dfMargin = pro.margin(start_date=beforeDate, end_date=nowDate)
    dfMargin = dfMargin[['trade_date', 'rzye']]
    MarginSum = {
        'trade_date': [],
        'rzye': []
    }
    dfMarginSum = pd.DataFrame(MarginSum)
    for i in range(len(dfMargin.index) - 1):
        a = dfMargin.iloc[i, 0]
        b = dfMargin.iloc[i + 1, 0]
        if a == b:
            temp = dfMargin.iloc[i, 1] + dfMargin.iloc[i + 1, 1]
            trade_date = a
            rzye = temp
            dfMarginSum = dfMarginSum.append(pd.DataFrame({'trade_date': [trade_date], 'rzye': [rzye]}))

    dfMarginSum['融资余额变动'] = dfMarginSum['rzye'] - dfMarginSum['rzye'].shift(-1)
    dfMarginSum = dfMarginSum[['trade_date', '融资余额变动']]
    dfMarginSumImg = dfMarginSum.plot(x='trade_date', title="融资余额变动", kind='bar')
    plt.sca(dfMarginSumImg)
    dfMarginSumImg = plt.gca().invert_xaxis()

    return dfMarginSumImg

def FullChangeHand():
    df = pro.index_dailybasic( start_date=lastTradeDate, end_date=nowDate, fields='ts_code,trade_date,turnover_rate,pe')
    dateinside = df.iloc[0,1]
    df = df[['ts_code','turnover_rate']]
    if dateinside == nowDate:
        resultimg = df.plot(kind = 'bar',x = 'ts_code',title=nowDate)
    else:
        resultimg = df.plot(kind = 'bar',x = 'ts_code',title=lastTradeDate)
    return resultimg

def CPI():
    dfCPI = pro.eco_cal(country='中国', event="中国CPI*")
    return dfCPI

def PPI():
    dfPMI = pro.eco_cal(country = '中国',event = "*PMI*")
    return dfPMI

def NotAgCareer():
    dfNotAg = pro.eco_cal(country='美国', event="*非农*")
    return dfNotAg


