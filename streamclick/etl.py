from clickhouse_driver import Client
from apis import Api, Oanda

types = ['currency', 'metal', 'cfd']

granularity = ['M2', 'M3', 'M4', 'M5', 'M10', 'M15', 'M30', 'H1']

def inst_insert(types, granularity, method):
    query = f'''insert into oanda.{types}_{granularity} values'''
    return clk.execute(query, [i for i in method])

clk = Client('click-server', port=9000)
oanda = Api(Oanda())
clk.execute('''insert into oanda.inst_info values''', [i for i in oanda.available()])

instrument = clk.execute('''select inst from oanda.inst_info''')

for t in types:
    for g in granularity:
        for inst in instrument:
            print(f'Download: {t} {inst} {g}')
            inst_insert(t, g, oanda.iter_price('2019-12-01 00:00:00', granularity=g, instrument=inst[0]))