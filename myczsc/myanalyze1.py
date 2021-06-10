from collections import OrderedDict
from data.ptdx import get_finance_overview
from myczsc.mysignals import check_eleven_fd, check_nine_fd, check_thirteen_fd
from typing import List
from czsc.analyze import CZSC, check_bi, check_fxs, remove_include
from czsc.enum import Direction, Mark, Signals
from czsc.objects import BI, NewBar, RawBar
from pytdx.hq import TdxHq_API
import numpy as np


def bars_to_array(bars: List[RawBar]):
    close_list = []
    for bar in bars:
        close_list.append(bar.close)
    return np.array(close_list)


class My_CZSC(CZSC):
    def __init__(self, bars: List[RawBar], freq: str, max_bi_count=30):
        """

        :param bars: K线数据
        :param freq: K线级别
        :param max_bi_count: 最大保存的笔数量
            默认值为 30，仅使用内置的信号和因子，不需要调整这个参数。
            如果进行新的信号计算需要用到更多的笔，可以适当调大这个参数。
        """
        # super().__init__(bars, freq, max_bi_count)
        self.max_bi_count = max_bi_count
        self.bars_raw = []  # 原始K线序列
        self.bars_ubi = []  # 未完成笔的无包含K线序列
        self.bi_list: List[BI] = []
        self.symbol = bars[0].symbol
        self.freq = freq
        self.close = np.array()
        
        for bar in bars:
            self.update(bar)
        #为屏蔽原库中每个update方法最后都会调用get_signals方法，不再调用super().__init__初始化
        self.signals = self.get_signals()
        self.signals.update(self.get_my_signals())
        # self.close = bars_to_array(bars)
        

    def get_my_signals(self):
        '''扩展CZSC类的get_signals得到的信号，区分B1、B2的详细情况'''
        s = OrderedDict({})
        s.update({
            "B1": Signals.Other.value,
            "B2": Signals.Other.value,
        })
        if self.signals['倒1表里关系'] in [Signals.BU0.value, Signals.BD0.value]:
            bis = self.bi_list
        else:
            bis = self.bi_list[:-1]
        #B1
        signal = check_nine_fd(bis[-9:])
        if signal[-2:] == 'B1':
            s['B1'] = signal
        signal = check_eleven_fd(bis[-11:])
        if signal[-2:] == 'B1':
            s['B1'] = signal
        signal = check_thirteen_fd(bis[-13:])
        if signal[-2:] == 'B1':
            s['B1'] = signal
        # B2
        signal = check_nine_fd(bis[-11:-2])
        if signal[-2:] == 'B1':
            s['B2'] = signal
        signal = check_eleven_fd(bis[-13:-2])
        if signal[-2:] == 'B1':
            s['B2'] = signal
        signal = check_thirteen_fd(bis[-15:-2])
        if signal[-2:] == 'B1':
            s['B2'] = signal

        #财务数据概况

        return s

    def update(self, bar: RawBar):
        """更新分析结果

        :param bar: 单根K线对象
        """
        # 更新K线序列
        if not self.bars_raw or bar.dt != self.bars_raw[-1].dt:
            self.bars_raw.append(bar)
            last_bars = [bar]
        else:
            self.bars_raw[-1] = bar
            last_bars = self.bars_ubi[-1].elements
            last_bars[-1] = bar
            self.bars_ubi.pop(-1)

        # 去除包含关系
        bars_ubi = self.bars_ubi
        for bar in last_bars:
            if len(bars_ubi) < 2:
                bars_ubi.append(
                    NewBar(symbol=bar.symbol,
                           dt=bar.dt,
                           open=bar.open,
                           close=bar.close,
                           high=bar.high,
                           low=bar.low,
                           vol=bar.vol,
                           elements=[bar]))
            else:
                k1, k2 = bars_ubi[-2:]
                has_include, k3 = remove_include(k1, k2, bar)
                if has_include:
                    bars_ubi[-1] = k3
                else:
                    bars_ubi.append(k3)
        self.bars_ubi = bars_ubi

        # 更新笔
        self.__update_bi()
        self.bi_list = self.bi_list[-self.max_bi_count:]
        if self.bi_list:
            sdt = self.bi_list[0].fx_a.elements[0].dt
            s_index = 0
            for i, bar in enumerate(self.bars_raw):
                if bar.dt >= sdt:
                    s_index = i
                    break
            self.bars_raw = self.bars_raw[s_index:]

    def __update_bi(self):
        bars_ubi = self.bars_ubi
        if len(bars_ubi) < 3:
            return

        # 查找笔
        if not self.bi_list:
            # 第一个笔的查找
            fxs = check_fxs(bars_ubi)
            if not fxs:
                return

            fx_a = fxs[0]
            fxs_a = [x for x in fxs if x.mark == fx_a.mark]
            for fx in fxs_a:
                if (fx_a.mark == Mark.D and fx.low <= fx_a.low) \
                        or (fx_a.mark == Mark.G and fx.high >= fx_a.high):
                    fx_a = fx
            bars_ubi = [x for x in bars_ubi if x.dt >= fx_a.elements[0].dt]

            bi, bars_ubi_ = check_bi(bars_ubi)
            if isinstance(bi, BI):
                self.bi_list.append(bi)
            self.bars_ubi = bars_ubi_
            return

        last_bi = self.bi_list[-1]

        # 如果上一笔被破坏，将上一笔的bars与bars_ubi进行合并
        min_low_ubi = min([x.low for x in bars_ubi[2:]])
        max_high_ubi = max([x.high for x in bars_ubi[2:]])

        if last_bi.direction == Direction.Up and max_high_ubi > last_bi.high:
            if min_low_ubi < last_bi.low and len(self.bi_list) > 2:
                bars_ubi_a = self.bi_list[-2].bars \
                            + [x for x in self.bi_list[-1].bars if x.dt > self.bi_list[-2].bars[-1].dt] \
                            + [x for x in bars_ubi if x.dt > self.bi_list[-1].bars[-1].dt]
                self.bi_list.pop(-1)
                self.bi_list.pop(-1)
            else:
                bars_ubi_a = last_bi.bars + [
                    x for x in bars_ubi if x.dt > last_bi.bars[-1].dt
                ]
                self.bi_list.pop(-1)
        elif last_bi.direction == Direction.Down and min_low_ubi < last_bi.low:
            if max_high_ubi > last_bi.high and len(self.bi_list) > 2:
                bars_ubi_a = self.bi_list[-2].bars \
                            + [x for x in self.bi_list[-1].bars if x.dt > self.bi_list[-2].bars[-1].dt] \
                            + [x for x in bars_ubi if x.dt > self.bi_list[-1].bars[-1].dt]
                self.bi_list.pop(-1)
                self.bi_list.pop(-1)
            else:
                bars_ubi_a = last_bi.bars + [
                    x for x in bars_ubi if x.dt > last_bi.bars[-1].dt
                ]
                self.bi_list.pop(-1)
        else:
            bars_ubi_a = bars_ubi

        if len(bars_ubi_a) > 300:
            print("{} - {} 未完成笔延伸超长，延伸数量: {}".format(self.symbol, self.freq,
                                                     len(bars_ubi_a)))
        bi, bars_ubi_ = check_bi(bars_ubi_a)
        self.bars_ubi = bars_ubi_
        if isinstance(bi, BI):
            self.bi_list.append(bi)
