import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,os
O=pathlib.Path(__file__).resolve().parent
print('actual_pid='+str(os.getpid()))
for name in sys.argv[1:]:
 p=O/('stageA.primary-readview-v2.'+name+'.txt')
 print('READVIEW V2 '+name+'\n'+p.read_text(encoding='utf-8'))
