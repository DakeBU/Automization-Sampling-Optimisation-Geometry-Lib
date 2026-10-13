from html.parser import HTMLParser

VOID_TAGS={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Node:
    def __init__(self,tag,attrs=None,parent=None):
        self.tag=tag;self.attrs=dict(attrs or []);self.parent=parent;self.children=[]
    def text(self):
        return ''.join(c.text() if isinstance(c,Node) else c for c in self.children)
    def descendants(self,tag=None,attr=None,value=None):
        result=[]
        for c in self.children:
            if not isinstance(c,Node):continue
            if (tag is None or c.tag==tag) and (attr is None or attr in c.attrs and (value is None or c.attrs[attr]==value)):result.append(c)
            result.extend(c.descendants(tag,attr,value))
        return result
    def class_has(self,name):return name in self.attrs.get('class','').split()
    def direct_code(self):
        for c in self.children:
            if isinstance(c,Node) and c.tag=='pre':
                for d in c.children:
                    if isinstance(d,Node) and d.tag=='code':return d
        return None
class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self,convert_charrefs=True);self.root=Node('root');self.stack=[self.root]
    def handle_starttag(self,tag,attrs):
        node=Node(tag,attrs,self.stack[-1]);self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:self.stack.append(node)
    def handle_startendtag(self,tag,attrs):
        node=Node(tag,attrs,self.stack[-1]);self.stack[-1].children.append(node)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:
                self.stack=self.stack[:i];break
    def handle_data(self,data):self.stack[-1].children.append(data)
def parse(text):
    p=Parser();p.feed(text.replace('\r\n','\n'));p.close();return p.root
