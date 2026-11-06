from control.pd_controller import PDController
from config.settings import load_config

class CascadeController:

    def __init__(self, kp_ext, kd_ext, kp_int, kd_int, dt):
        self.pd_interno = PDController(kp_int, kd_int, dt)
        self.pd_externo = PDController(kp_ext, kd_ext, dt)

    def compute(self, phi_ref, phi, theta, volt_limit):
        erro_pendulo = phi_ref - phi
        theta_ref = self.pd_externo.compute(erro_pendulo)
        erro_braco = theta_ref - theta
        tensao = self.pd_interno.compute(erro_braco)
        
        tensao = max(-volt_limit, min(volt_limit,tensao))
        return tensao

    def reset(self):
        self.pd_interno.reset()
        self.pd_externo.reset()

