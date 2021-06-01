# coding: utf-8

from typing import List, Union
from czsc.objects import Direction, BI, FakeBI
from czsc.enum import Signals

def check_nine_fd(fds: List[Union[BI, FakeBI]]) -> str:
    """识别九段形态

    :param fds: list
        由远及近的九段形态
    :return: str
    """
    v = Signals.Other.value
    if len(fds) != 9:
        return v

    direction = fds[-1].direction
    fd1, fd2, fd3, fd4, fd5, fd6, fd7, fd8, fd9 = fds
    max_high = max([x.high for x in fds])
    min_low = min([x.low for x in fds])

    if direction == Direction.Down:
        if min_low == fd9.low and max_high == fd1.high:
            # aAbBc式底背驰
            if min(fd2.high, fd4.high) > max(fd2.low, fd4.low) > fd6.high \
                    and min(fd6.high, fd8.high) > max(fd6.low, fd8.low) \
                    and min(fd2.low, fd4.low) > max(fd6.high, fd8.high) \
                    and fd9.power < fd5.power:
                v = 'X9B1'
    elif direction == Direction.Up:
        if max_high == fd9.high and min_low == fd1.low:
            # aAbBc式顶背驰
            if fd6.low > min(fd2.high, fd4.high) > max(fd2.low, fd4.low) \
                    and min(fd6.high, fd8.high) > max(fd6.low, fd8.low) \
                    and max(fd2.high, fd4.high) < min(fd6.low, fd8.low) \
                    and fd9.power < fd5.power:
                v = 'X9S1'
    else:
        raise ValueError("direction 的取值错误")
    return v


def check_eleven_fd(fds: List[Union[BI, FakeBI]]) -> str:
    """识别十一段形态

    :param fds: list
        由远及近的十一段形态
    :return: str
    """
    v = Signals.Other.value
    if len(fds) != 11:
        return v

    direction = fds[-1].direction
    fd1, fd2, fd3, fd4, fd5, fd6, fd7, fd8, fd9, fd10, fd11 = fds
    max_high = max([x.high for x in fds])
    min_low = min([x.low for x in fds])

    if direction == Direction.Down:
        if min_low == fd11.low and max_high == fd1.high:
            # aAbBc式底背驰，fd2-fd6构成A
            if min(fd2.high, fd4.high, fd6.high) > max(fd2.low, fd4.low, fd6.low) > fd8.high \
                    and min(fd8.high, fd10.high) > max(fd8.low, fd10.low) \
                    and min(fd2.low, fd4.low, fd6.low) > max(fd8.high, fd10.high) \
                    and fd11.power < fd7.power:
                v = 'X11B1'

            # aAbBc式底背驰，fd6-fd10构成B
            if min(fd2.high, fd4.high) > max(fd2.low, fd4.low) > fd6.high \
                    and min(fd6.high, fd8.high, fd10.high) > max(fd6.low, fd8.low, fd10.low) \
                    and min(fd2.low, fd4.low) > max(fd6.high, fd8.high, fd10.high) \
                    and fd11.power < fd5.power:
                v = 'X11B1'
    elif direction == Direction.Up:
        if max_high == fd11.high and min_low == fd1.low:
            # aAbBC式顶背驰，fd2-fd6构成A
            if fd8.low > min(fd2.high, fd4.high, fd6.high) >= max(fd2.low, fd4.low, fd6.low) \
                    and min(fd8.high, fd10.high) >= max(fd8.low, fd10.low) \
                    and max(fd2.high, fd4.high, fd6.high) < min(fd8.low, fd10.low) \
                    and fd11.power < fd7.power:
                v = 'X11S1'

            # aAbBC式顶背驰，fd6-fd10构成B
            if fd6.low > min(fd2.high, fd4.high) >= max(fd2.low, fd4.low) \
                    and min(fd6.high, fd8.high, fd10.high) >= max(fd6.low, fd8.low, fd10.low) \
                    and max(fd2.high, fd4.high) < min(fd6.low, fd8.low, fd10.low) \
                    and fd11.power < fd7.power:
                v = 'X11S1'
    else:
        raise ValueError("direction 的取值错误")
    return v


def check_thirteen_fd(fds: List[Union[BI, FakeBI]]) -> str:
    """识别十三段形态

    :param fds: list
        由远及近的十三段形态
    :return: str
    """
    v = Signals.Other.value
    if len(fds) != 13:
        return v

    direction = fds[-1].direction
    fd1, fd2, fd3, fd4, fd5, fd6, fd7, fd8, fd9, fd10, fd11, fd12, fd13 = fds
    max_high = max([x.high for x in fds])
    min_low = min([x.low for x in fds])

    if direction == Direction.Down:
        if min_low == fd13.low and max_high == fd1.high:
            # aAbBc式底背驰，fd2-fd6构成A，fd8-fd12构成B
            if min(fd2.high, fd4.high, fd6.high) > max(fd2.low, fd4.low, fd6.low) > fd8.high \
                    and min(fd8.high, fd10.high, fd12.high) > max(fd8.low, fd10.low, fd12.low) \
                    and min(fd2.low, fd4.low, fd6.low) > max(fd8.high, fd10.high, fd12.high) \
                    and fd13.power < fd7.power:
                v = 'X13B1'
    elif direction == Direction.Up:
        if max_high == fd13.high and min_low == fd1.low:
            # aAbBC式顶背驰，fd2-fd6构成A，fd8-fd12构成B
            if fd8.low > min(fd2.high, fd4.high, fd6.high) >= max(fd2.low, fd4.low, fd6.low) \
                    and min(fd8.high, fd10.high, fd12.high) >= max(fd8.low, fd10.low, fd12.low) \
                    and max(fd2.high, fd4.high, fd6.high) < min(fd8.low, fd10.low, fd12.low) \
                    and fd13.power < fd7.power:
                v = 'X13S1'
    else:
        raise ValueError("direction 的取值错误")
    return v
