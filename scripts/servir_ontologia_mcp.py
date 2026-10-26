"""Proxy stdio del MCP compartido: un backend persistente para varios agentes."""
import json
import sys
from mcp_compartido import ALLOW, Cliente, conectar, verificar_consulta


def main():
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    active = conectar()
    client = Cliente(active.url, active.headers['Authorization'][7:])
    active.cerrar()
    for line in sys.stdin:
        message = None
        try:
            message = json.loads(line)
            method = message.get('method', '')
            if method not in {'initialize', 'notifications/initialized', 'notifications/cancelled', 'tools/list', 'tools/call', 'ping'}:
                raise ValueError('Método MCP no permitido')
            if method == 'tools/call':
                params = message['params']
                if params['name'] not in ALLOW.split(','):
                    raise ValueError('Herramienta fuera del contrato')
                if params['name'] == 'onto_query':
                    verificar_consulta(params['arguments']['query'])
            result = client.enviar(message)
            if result is not None and 'id' in message:
                print(json.dumps(result, ensure_ascii=False), flush=True)
        except Exception as exc:
            if message is not None and 'id' in message:
                print(json.dumps({'jsonrpc': '2.0', 'id': message['id'], 'error': {'code': -32602, 'message': str(exc)}}), flush=True)
            else:
                print(str(exc), file=sys.stderr)
    client.cerrar()


if __name__ == '__main__':
    main()
