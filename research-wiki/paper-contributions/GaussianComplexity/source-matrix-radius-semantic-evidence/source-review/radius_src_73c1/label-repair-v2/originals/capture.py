import sys,subprocess,json,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent
cmd=sys.argv[1:]
r=subprocess.run(cmd,cwd="/Users/zhouhuanjian/ASTIS-GC",text=True,capture_output=True)
rec={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"cmd":cmd,"cwd":"/Users/zhouhuanjian/ASTIS-GC","returncode":r.returncode,"stdout":r.stdout,"stderr":r.stderr}
with (ROOT/"raw_commands.jsonl").open("a") as f: f.write(json.dumps(rec)+"\n")
print(r.stdout,end="")
print(r.stderr,end="",file=sys.stderr)
sys.exit(r.returncode)
