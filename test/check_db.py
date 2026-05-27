import json, os, sys
sys.path.insert(0, os.path.abspath('.'))

from lendingModules import dbOperations

# Lue settings.json
with open('settings.json', 'r', encoding='utf-8') as f:
    s = json.load(f)

print('settings.json department:', s.get('department') or s.get('osasto'))

dbSettings = {
    'server': s.get('server'),
    'port': s.get('port'),
    'database': s.get('database'),
    'userName': s.get('userName'),
    'password': s.get('password'),
}
print('DB settings host/port/db:', dbSettings['server'], dbSettings['port'], dbSettings['database'])

db = dbOperations.DbConnection(dbSettings)

for table in ('vapaana', 'ajossa'):
    try:
        cols = db.readTableColumns(table)
        print(f'\n{table} columns:', cols)
    except Exception as e:
        print(f'\nFailed to read columns for {table}:', e)

dept = s.get('department') or s.get('osasto')
try:
    print('\nUsing department:', dept)
    free = db.getVehiclesFree(dept) if dept else db.readAllColumnsFromTable('vapaana')
    inuse = db.getVehiclesInUse(dept) if dept else db.readAllColumnsFromTable('ajossa')
    print('getVehiclesFree rows:', len(free))
    print('getVehiclesInUse rows:', len(inuse))
    print('sample free:', free[:5])
    print('sample inuse:', inuse[:5])
except Exception as e:
    print('Error when calling getVehicles*: ', type(e).__name__, e)