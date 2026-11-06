import numpy as np

class RLSupervisor:
    def __init__(self, sac_agent, ppo_agent, fixed_ref =np.pi):
        self.sac = sac_agent
        self.ppo = ppo_agent
        self.fixed_ref = fixed_ref
    
    def get_reference(self, obs: np.ndarray) -> float:
        sac_ref = self.sac.get_action(obs)
        choice = self.ppo.get_action(obs)
        return self.fixed_ref if choice == 1 else sac_ref