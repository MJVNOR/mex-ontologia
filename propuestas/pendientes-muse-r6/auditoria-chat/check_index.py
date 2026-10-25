import hashlib
p = 'propuestas/pendientes-muse-r6/chat-diagnostico/codigo/index.ts'
s = open(p, 'rb').read()
print('CRLF:', s.count(b'\r\n'), 'LF:', s.count(b'\n'))
print('sha lf-only:', hashlib.sha256(s.replace(b'\r\n', b'\n')).hexdigest())
t = s.decode('utf-8')
marks = ['const miss = await answerOnce(', "send({ type: 'error'", 'async function runTurn',
         'await runTurn(step.prompt)', 'writeChatCache(', 'minIntervalMs',
         'exigirRespuestaVisible(result.text', 'return runTurn(question);',
         'return await runTurn(context);', 'stripThoughtBlocks', '...']
for m in marks:
    print(repr(m), t.count(m))
