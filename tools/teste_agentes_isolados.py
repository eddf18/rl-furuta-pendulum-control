import numpy as np
from agents.sac_agent import SACAgent
from agents.ppo_agent import PPOAgent

print("Carregando SAC...")
sac = SACAgent("agents/weights/sac_actor_swingup.onnx")
print("SAC carregado com sucesso.")

print("Carregando PPO...")
ppo = PPOAgent("agents/weights/ppo_actor_mode.onnx")
print("PPO carregado com sucesso.")

obs_teste = [0, 1, 0, -1, 0, 0]

phi_ref = sac.get_action(obs_teste)
modo = ppo.get_action(obs_teste)

print(f"SAC -> phi_ref: {phi_ref:.4f} rad")
print(f"PPO -> modo: {modo}")