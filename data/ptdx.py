from pytdx.hq import TdxHq_API

api = TdxHq_API()

with api.connect('119.147.212.81', 7709):
    # slist=api.get_security_list(1, 0)
    s=api.get_finance_info(0, '000001')
    print(s)