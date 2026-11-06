import time
import math
import pigpio

from hardware.encoder import QuadratureEncoder
from hardware.motor import QUBEMotor

def test_encoders(pi):
    enc_pendulo = QuadratureEncoder(pi, 11, 8, 512)
    enc_braco = QuadratureEncoder(pi, 6, 5, 512)

    print("Gire os eixos manualmente - 10 segundos")
    t_start = time.perf_counter()
    while time.perf_counter() - t_start < 10:
        print(f"Braço: {enc_braco.angle_rad:+.3f} rad | "
              f"Pêndulo: {enc_pendulo.angle_rad:+.3f} rad", end = "\r")
        time.sleep(0.05)
    
    enc_braco.cancel()
    enc_pendulo.cancel()

def test_motor(pi):
    # nao sei fazer teste de rampa
    motor = QUBEMotor(pi, 12, 17, 27, 20000)
    motor.release_brake()

    # rampa positiva
    print("Rampa positiva")
    for v in [3.0, 6.0, 9.0, 12.0]:
        print(f" {v}V")
        motor.set_voltage(v, 12.0)
        time.sleep(2)

    motor.stop()
    time.sleep(0.5)

    #rampa negativa
    print("Rampa negativa")
    for v in [-3.0, -6.0, -9.0, -12.0]:
        print(f" {v}V")
        motor.set_voltage(v, 12.0)
        time.sleep(2)

    motor.stop()
    time.sleep(0.5)

    # teste de freio
    print("Teste de freio")
    motor.set_voltage(6.0, 12.0)
    time.sleep(1)
    motor.brake()
    time.sleep(2)
    motor.release_brake()
    time.sleep(0.5)

    motor.shutdown()

if __name__ == "__main__":
    pi = pigpio.pi()
    if not pi.connected:
        raise RuntimeError("pigpio não está rodando")
    try:
        test_encoders(pi)
        test_motor(pi)
    finally:
        pi.stop()