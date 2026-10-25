import re
t = open('propuestas/pendientes-muse-r6/chat-diagnostico/codigo/index.ts', encoding='utf-8').read()
for m in re.finditer(r'\.\.\.', t):
    s = max(0, m.start() - 90)
    print(repr(t[s:m.end() + 60]))
    print('---')
