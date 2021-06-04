from collections import OrderedDict
from data.ptdx import get_finance_overview
from myczsc.mysignals import check_eleven_fd, check_nine_fd, check_thirteen_fd
from typing import List
from czsc.analyze import CZSC
from czsc.enum import Signals
from czsc.objects import RawBar
from pytdx.hq import TdxHq_API


class My_CZSC(CZSC):
    def __init__(self, bars: List[RawBar], freq: str, max_bi_count=30):
        super().__init__(bars, freq, max_bi_count)
        self.signals.update(self.get_my_signals())

    def get_my_signals(self):
        '''扩展CZSC类的get_signals得到的信号'''
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
