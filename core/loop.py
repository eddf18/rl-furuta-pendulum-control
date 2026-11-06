import time
import math
import pigpio

from hardware.encoder import QuadratureEncoder
from hardware.motor import QUBEMotor
from core.observer import Observer
from control.controle_cascata import CascadeController
from agents.sac_agent import SACAgent
from agents.ppo_agent import PPOAgent
from agents.rl_supervisor import RLSupervisor
from config.settings import load_config

class ControlLoop:

    def __init__(self):
        cfg = load_config()  # ← dentro do __init__

        self.dt       = cfg["control"]["dt"]
        self.volt_limit = cfg["control"]["volt_limit"]

        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("pigpiod não está rodando")

        self.enc_braco   = QuadratureEncoder(self.pi,
            cfg["hardware"]["encoders"]["arm"]["pin_a"],
            cfg["hardware"]["encoders"]["arm"]["pin_b"],
            cfg["hardware"]["encoders"]["arm"]["ppr"])

        self.enc_pendulo = QuadratureEncoder(self.pi,
            cfg["hardware"]["encoders"]["pendulum"]["pin_a"],
            cfg["hardware"]["encoders"]["pendulum"]["pin_b"],
            cfg["hardware"]["encoders"]["pendulum"]["ppr"])

        self.motor = QUBEMotor(self.pi,
            cfg["hardware"]["motor"]["pwm_pin"],
            cfg["hardware"]["motor"]["dir_pin"],
            cfg["hardware"]["motor"]["brake_pin"],
            cfg["hardware"]["motor"]["frequency"])

        self.observer = Observer(self.enc_braco, self.enc_pendulo, self.dt)

        self.cascata = CascadeController(
            kp_ext = cfg["control"]["pd_externo"]["kp"],
            kd_ext = cfg["control"]["pd_externo"]["kd"],
            kp_int = cfg["control"]["pd_interno"]["kp"],
            kd_int = cfg["control"]["pd_interno"]["kd"],
            dt     = self.dt)

        # Agentes de RL

        self.sac_agent = SACAgent(cfg["agents"]["sac_path"])
        self.ppo_agent = PPOAgent(cfg["agents"]["ppo_path"])
        self.rl_supervisor = RLSupervisor(self.sac_agent, self.ppo_agent, fixed_ref=cfg["agents"]["phi_ref"])

        self.rl_decimation = round(cfg["agents"]["dt"]/self.dt) # o que essa parte faz?
        self._step_count = 0
        self._phi_ref_cache = cfg["agents"]["phi_ref"] #valor inical neutro?
        self._arm_max = cfg["control"]["angle_limit"]["arm_max"]
        self._arm_min = cfg["control"]["angle_limit"]["arm_min"]
        self._running = False

    def start(self):
        self.motor.release_brake()
        self._running = True
        try:
            self._loop()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def _loop(self):
        while self._running:
            t_start = time.perf_counter()
            self._step()
            elapsed = time.perf_counter() - t_start
            time.sleep(max(0, self.dt - elapsed))

    def _step(self):
        self.observer.update() # lê os encoders e atualiza o estado
        obs = self.observer.observation

        if self._step_count % self.rl_decimation == 0:
            self._phi_ref_cache = self.rl_supervisor.get_reference(obs)
        self._step_count += 1
        
        phi_ref = self._phi_ref_cache
        phi = self.observer.phi
        theta = self.observer.theta
        tensao = self.cascata.compute(phi_ref, phi, theta, self.volt_limit)
        
        # limitador (deveria para o motor ou tentar jogar o pêndulo para o outro lado?)
        print(f"theta: {theta:+.3f} limite: +/-{self._arm_max:.3f}")

        if theta > self._arm_max or theta < self._arm_min:
            print("LIMITE ATINGIDO - parando motor!")
            self.stop()
            return

        self.motor.set_voltage(tensao, self.volt_limit)

    def stop(self):
        self._running = False
        self.motor.stop()
        self.motor.brake()