# coding: utf-8

from myczsc.mytrader import CzscTrader
from data.tdx import get_data_from_tdxfile
import sys
sys.path.insert(0, ".")
sys.path.insert(0, "..")

from datetime import datetime
import czsc


from czsc.analyze import CZSC



def by_czsc():
    bars = get_data_from_tdxfile('300049', 'sz')
    c = CZSC(bars, freq="日线")
    c.to_echarts()
    c.open_in_browser()


def by_CzscFactors():
    ct = CzscTrader(symbol="000001", max_count=800, end_date=datetime.now())
    # max_count 参数控制获取的K线数量
    # end_date  参数控制获取K线的截止时间，便于查看历史分析结果，默认为当下时间
    # 可视化分析结果
    # chart = ct.kf.take_snapshot(width="900px", height="480px")
    # chart.render_notebook()
    ct.open_in_browser(width="1400px", height="580px")
    # 调用选股方法判断是否有满足的选股条件
    # ct.run_selector()
    # print(ct.run_selector())

if __name__ == '__main__':
    by_czsc()
    # by_CzscFactors()
