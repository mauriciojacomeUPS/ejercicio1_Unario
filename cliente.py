import grpc
import pagos_pb2
import pagos_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pagos_pb2_grpc.ValidadorPagosStub(channel)

        # Cuatro casos de prueba con numeros ficticios
        casos = [
            pagos_pb2.SolicitudPago(
                id_transaccion="TX-1001",
                numero_tarjeta="1111222233334444",
                monto=250,
                codigo_moneda="USD",
                pais_origen="EC"
            ),
            pagos_pb2.SolicitudPago(
                id_transaccion="TX-1002",
                numero_tarjeta="1111222233334444",
                monto=-50,
                codigo_moneda="USD",
                pais_origen="EC"
            ),
            pagos_pb2.SolicitudPago(
                id_transaccion="TX-1003",
                numero_tarjeta="4000111122223333",
                monto=120,
                codigo_moneda="USD",
                pais_origen="US"
            ),
            pagos_pb2.SolicitudPago(
                id_transaccion="TX-1004",
                numero_tarjeta="1111222233334444",
                monto=12500,
                codigo_moneda="USD",
                pais_origen="EC"
            )
        ]

        for peticion in casos:
            print(f"\n[Cliente] Transaccion: {peticion.id_transaccion}")

            try:
                respuesta = stub.VerificarTransaccion(peticion)

                if respuesta.aprobado:
                    print(f"APROBADO: {respuesta.codigo_autorizacion}")
                else:
                    print(f"RECHAZADO: {respuesta.motivo_rechazo}")

            except grpc.RpcError as e:
                print(f"[Error gRPC] Codigo: {e.code()} | Detalle: {e.details()}")


if __name__ == "__main__":
    run()
