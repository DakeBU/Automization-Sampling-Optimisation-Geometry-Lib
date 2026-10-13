import subprocess,sys
py=sys.executable
for label,file in [('final-gates','final-gates75.py'),('record-final','record-integration75.py'),('pr-body','write-pr75.py'),('freeze-final-reader','freeze-final-reader75.py')]:
 args=['final'] if label=='record-final' else []
 subprocess.run([py,'-B','-X','utf8','.astis/pbps-clock75/foreground75.py','integration75/'+label,py,'-B','-X','utf8','.astis/pbps-clock75/'+file,*args],check=True)
