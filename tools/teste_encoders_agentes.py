import time
import pigpio

from hardware.encoder import QuadratureEncoder
from core.observer import Observer
from agents.sac_agent import SACAgent
from agents.ppo_agent import PPOAgent
from agents.rl_supervisor import RLSupervisor


pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio não está rodando")

enc_braco = QuadratureEncoder(pi, 9, 25, 512)
enc_pendulo = QuadratureEncoder(pi, 6, 5, 512)

dt = 0.02
observer = Observer(enc_braco, enc_pendulo, dt)

sac = SACAgent("agents/weights/sac_actor_swingup.onnx")
ppo = PPOAgent("agents/weights/ppo_actor_mode.onnx")
supervisor = RLSupervisor(sac, ppo, fixed_ref=3.14159)

print("IMPORTANTE: motor NÃO está sendo acionado neste teste.")
print("Gire o braço e o pêndulo manualmente e observe a saída.")
print("Ctrl+C para parar.\n")

try:
    while True:
        observer.update()
        obs = observer.observation
        phi_ref = supervisor.get_reference(obs)
        modo = ppo.get_action(obs)

        print(f"theta: {observer.theta:+.3f} | phi: {observer.phi:+.3f} | "
              f"phi_ref: {phi_ref:+.3f} | modo: {modo}", end="\r")

        time.sleep(dt)

except KeyboardInterrupt:
    print("\nTeste encerrado.")
finally:
    enc_pendulo.cancel()
    enc_braco.cancel()
    pi.stop()