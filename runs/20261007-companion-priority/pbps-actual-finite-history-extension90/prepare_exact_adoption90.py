from pathlib import Path
r=Path(__file__).parent
s=(r.parent/'pbps-actual-conditional-next-wait-density89/adopt_exact89.py').read_text(encoding='utf8').replace('89','90').replace('actual-conditional-next-wait-density','actual-finite-history-extension').replace('pbps-conditional-next-wait-density-preread90','pbps-next-history-extension-preread90')
for old,new in [('e544dbd8400b4cc3a47ff8f4632ab97045efb496bd7bf636d61fcebe41aefd65','26ea4bf0423f71453dbfb770776337e1b97c9585e45431b6e9153921550ca51a'),('99daaca67e4b6587cfd9f1d5ead8a27c1a49f2b45599b4286718b1cce9ecaa97','a9aea567852cc0735120909a5626f8287f5bd87394ae5aed65e9e2d346788666'),('0cfb0f6f3f89806303ec11a720fdef6c7835089c8b6e19d3fa9e4938142ee3d3','6008aa04b9154f839d5fc41a18bc1ca9b5131f29d61e82f84a054993478c3fc3'),('58ddf518b7c75537680526fa809624ac7fe0b4c7','e8d38b3002f4562ef254205135c0d213f9efe410')]:
 assert old in s,old;s=s.replace(old,new)
p=r/'adopt_exact90.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
