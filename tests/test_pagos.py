import unittest
from concurrent import futures

import grpc
import pagos_pb2
import pagos_pb2_grpc
from servidor import ValidadorPagosServicer


class PruebasPagos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        pagos_pb2_grpc.add_ValidadorPagosServicer_to_server(
            ValidadorPagosServicer(), cls.server
        )
        puerto = cls.server.add_insecure_port("127.0.0.1:0")
        cls.server.start()
        cls.channel = grpc.insecure_channel(f"127.0.0.1:{puerto}")
        cls.stub = pagos_pb2_grpc.ValidadorPagosStub(cls.channel)

    @classmethod
    def tearDownClass(cls):
        cls.channel.close()
        cls.server.stop(0).wait()

    def solicitud(self, monto=250, tarjeta="1111222233334444", pais="EC"):
        return pagos_pb2.SolicitudPago(
            id_transaccion="TX-PRUEBA",
            numero_tarjeta=tarjeta,
            monto=monto,
            codigo_moneda="USD",
            pais_origen=pais
        )

    def test_pago_aprobado(self):
        respuesta = self.stub.VerificarTransaccion(self.solicitud())
        self.assertTrue(respuesta.aprobado)
        self.assertTrue(respuesta.codigo_autorizacion.startswith("AUTH-"))

    def test_monto_invalido(self):
        with self.assertRaises(grpc.RpcError) as error:
            self.stub.VerificarTransaccion(self.solicitud(monto=-50))
        self.assertEqual(error.exception.code(), grpc.StatusCode.INVALID_ARGUMENT)

    def test_tarjeta_bloqueada(self):
        with self.assertRaises(grpc.RpcError) as error:
            self.stub.VerificarTransaccion(
                self.solicitud(tarjeta="4000111122223333")
            )
        self.assertEqual(error.exception.code(), grpc.StatusCode.PERMISSION_DENIED)

    def test_rechazo_por_politica(self):
        respuesta = self.stub.VerificarTransaccion(self.solicitud(monto=12500))
        self.assertFalse(respuesta.aprobado)
        self.assertIn("10000", respuesta.motivo_rechazo)


if __name__ == "__main__":
    unittest.main()
