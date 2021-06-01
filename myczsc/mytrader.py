# coding: utf-8
from data.tdx import format_kline
from czsc.factors.factors import CzscFactors, factors_func
from czsc.utils.kline_generator import KlineGeneratorBy1Min
import pandas as pd
from datetime import datetime, timedelta
# from czsc.czsc.factors import KlineGeneratorBy1Min, CzscFactors, factors_func
# from ..data.jq import get_kline, get_kline_period
from data.base import freq_inv
from mootdx.quotes import Quotes


class CzscTrader:
    """缠中说禅股票 选股/择时"""
    def __init__(self, symbol, max_count=1000, end_date=None):
        """
        :param symbol:
        """
        self.symbol = symbol
        if end_date:
            self.end_date = pd.to_datetime(end_date)
        else:
            self.end_date = datetime.now()
        self.max_count = max_count

        client = Quotes.factory(market='std')  # 标准市场
        # client = Quotes.factory(market='ext', multithread=True, heartbeat=True) # 扩展市场

        kg = KlineGeneratorBy1Min(
            max_count=max_count * 2,
            freqs=['1分钟', '5分钟', '15分钟', '30分钟', '60分钟', '日线'])
        for freq in kg.freqs:
            # print(symbol, freq_inv[freq],max_count)
            quote = client.bars(symbol,
                                frequency=freq_inv[freq],
                                offset=max_count)
            bars = format_kline(symbol, quote)
            kg.init_kline(freq, bars)
        kf = CzscFactors(kg, factors=factors_func)
        self.kf = kf
        self.s = kf.s
        self.freqs = kg.freqs

    def __repr__(self):
        return "<CzscTrader of {} @ {}>".format(self.symbol, self.kf.end_dt)

    def take_snapshot(self, file_html, width="1400px", height="680px"):
        self.kf.take_snapshot(file_html, width, height)

    def open_in_browser(self, width="1400px", height="580px"):
        self.kf.open_in_browser(width, height)

    def update_factors(self):
        """更新K线数据到最新状态"""
        client = Quotes.factory(market='std')  # 标准市场
        quote = client.bars(self.symbol,
                                frequency=7,
                                offset=max_count)
        bars = format_kline(symbol, quote)
        bars = get_kline_period(symbol=self.symbol,
                                start_date=self.kf.end_dt,
                                end_date=datetime.now(),
                                freq="1min")
        if not bars:
            return
        for bar in bars:
            self.kf.update_factors(bar)
        self.s = self.kf.s

    def forward(self, n: int = 3):
        """向前推进N天"""
        ed = self.kf.end_dt + timedelta(days=n)
        if ed > datetime.now():
            print(f"{ed} > {datetime.now()}，无法继续推进")
            return

        bars = get_kline_period(symbol=self.symbol,
                                start_date=self.kf.end_dt,
                                end_date=ed,
                                freq="1min")
        if not bars:
            print(f"{self.kf.end_dt} ~ {ed} 没有交易数据")
            return

        for bar in bars:
            self.kf.update_factors(bar)

        self.s = self.kf.s
        self.end_date = self.kf.end_dt.date()
