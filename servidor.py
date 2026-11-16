from concurrent import futures
import grpc
import uuid
import pagos_pb2
import pagos_pb2_grpc


class ValidadorPagosServicer(pagos_pb2_grpc.ValidadorPagosServicer):
    def VerificarTransaccion(self, request, context):
        print(f"[Servidor] Transaccion: {request.id_transaccion}")
        print(f"Monto: {request.monto} {request.codigo_moneda}")

        tarjeta = request.numero_tarjeta

        # Regla 1: Datos invalidos
        if request.monto <= 0 or len(tarjeta) != 16 or not tarjeta.isascii() or not tarjeta.isdecimal():
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Monto o numero de tarjeta invalido"
            )

        # Regla 2: Tarjeta bloqueada
        if tarjeta.startswith("4000"):
            context.abort(
                grpc.StatusCode.PERMISSION_DENIED,
                "Tarjeta bloqueada por fraude"
            )

        # Regla 3: Monto alto fuera de US y MX
        if request.monto > 10000 and request.pais_origen.upper() not in ("US", "MX"):
            return pagos_pb2.ResultadoPago(
                aprobado=False,
                motivo_rechazo="Monto mayor a 10000 fuera de US/MX"
            )

        # Pago aprobado
        codigo = "AUTH-" + uuid.uuid4().hex[:8].upper()

        return pagos_pb2.ResultadoPago(
            aprobado=True,
            codigo_autorizacion=codigo,
            motivo_rechazo=""
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pagos_pb2_grpc.add_ValidadorPagosServicer_to_server(
        ValidadorPagosServicer(), server
    )
    puerto = "50051"
    server.add_insecure_port(f"[::]:{puerto}")
    server.start()
    print(f"Servidor gRPC escuchando en el puerto {puerto}...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
