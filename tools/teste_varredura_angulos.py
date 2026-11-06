# tools/teste_varredura_angulos.py
import numpy as np
from agents.sac_agent import SACAgent
from agents.ppo_agent import PPOAgent

sac = SACAgent("agents/weights/sac_actor_swingup.onnx")
ppo = PPOAgent("agents/weights/ppo_actor_mode.onnx")

print(f"{'theta':>8} {'phi':>8} {'phi_ref (SAC)':>15} {'modo (PPO)':>12}")
print("-" * 50)

theta_fixo = 0.0
for phi_deg in range(0, 361, 30):
    phi = np.deg2rad(phi_deg)
    obs = [np.sin(theta_fixo), np.cos(theta_fixo), np.sin(phi), np.cos(phi), 0.0, 0.0]

    phi_ref = sac.get_action(obs)
    modo = ppo.get_action(obs)

    print(f"{theta_fixo:8.2f} {phi:8.2f} {phi_ref:15.4f} {modo:12d}")