# Ejercicio 1 - gRPC Unario: Validador de Pagos

**Estudiante:** Mauricio Jácome  
**Tema:** Programación Distribuida - gRPC unario con Python

Este ejercicio simula la validación de pagos mediante una comunicación **unaria**: el cliente envía una solicitud y el servidor devuelve una respuesta.

## Archivos

- `pagos.proto`: contrato Protobuf del servicio `ValidadorPagos`.
- `servidor.py`: aplica las reglas de validación y devuelve resultados o errores gRPC.
- `cliente.py`: ejecuta cuatro casos de prueba.
- `requirements.txt`: dependencias del proyecto.
- `.gitignore`: excluye archivos locales y temporales.

Los archivos `pagos_pb2.py` y `pagos_pb2_grpc.py` **no se almacenan**: se generan con `protoc`.

## Instalación (Ubuntu)

```bash
git clone https://github.com/mauriciojacomeUPS/ejercicio1_Unario.git
cd ejercicio1_Unario
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pagos.proto
```

## Ejecución

En la **primera terminal**:

```bash
source .venv/bin/activate
python servidor.py
```

En la **segunda terminal**, dentro de la misma carpeta:

```bash
source .venv/bin/activate
python cliente.py
```

El servidor utiliza el puerto **50051**. Debe estar ejecutándose antes de iniciar el cliente.

## Casos de prueba

| Transacción | Escenario | Resultado esperado |
| --- | --- | --- |
| TX-1001 | Monto 250 USD, tarjeta con 16 dígitos | Aprobado con código `AUTH-...` |
| TX-1002 | Monto negativo | Error `INVALID_ARGUMENT` |
| TX-1003 | Tarjeta que inicia con 4000 | Error `PERMISSION_DENIED` |
| TX-1004 | Monto 12500 USD desde EC | Rechazo de negocio (`aprobado=False`) |

## Reglas implementadas

1. Se rechazan montos menores o iguales a cero y tarjetas que no tengan exactamente 16 dígitos ASCII.
2. Se bloquean las tarjetas que comienzan con `4000`.
3. Los montos mayores a 10000 cuyo país no sea `US` o `MX` reciben un rechazo de negocio.
4. Si se cumplen las condiciones anteriores, se devuelve un código de autorización aleatorio.

> **Nota:** Programa educativo con tarjetas ficticias. No realiza pagos reales, no integra pasarelas de pago ni cifra la conexión gRPC.

## Trazabilidad

Cada parte se incorporó en un commit distinto:

1. `feat(proto)`: definición del contrato y mensajes.
2. `feat(server)`: implementación de las reglas y estados gRPC.
3. `feat(client)`: pruebas de las cuatro transacciones.
4. `chore`: dependencias e ignorados del proyecto.
5. `docs`: instrucciones de instalación, ejecución y pruebas.

Consulta el historial en [Commits](https://github.com/mauriciojacomeUPS/ejercicio1_Unario/commits/main).
