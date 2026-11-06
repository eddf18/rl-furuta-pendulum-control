import time
import pigpio

from hardware.encoder import QuadratureEncoder

def calibrate(pi):
    enc_pendulo = QuadratureEncoder(pi, 11, 8, 512)
    enc_braco = QuadratureEncoder(pi, 6, 5, 512)


    input("Posicione o sistema no ponto ZERO e pressione ENTER para calibrar...")

    enc_braco.reset()
    enc_pendulo.reset()

    print(f"Braço: {enc_braco.angle_rad:.4f} rad")
    print(f"Pendulo: {enc_pendulo.angle_rad:.4f} rad")

    enc_pendulo.cancel()
    enc_braco.cancel()

if __name__ == "__main__":
    pi = pigpio.pi()
    if not pi.connected:
        raise RuntimeError("pigpio não está rodando")
    
    try:
        calibrate(pi)
    finally:
        pi.stop()