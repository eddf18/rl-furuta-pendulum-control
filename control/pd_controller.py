# Controlador PD

class PDController:
    def __init__(self, kp, kd, dt):

        self.Kp = kp
        self.Kd = kd

        self.dt = dt
        self.erro_anterior = 0

    def compute(self, erro):

        derivada = (erro - self.erro_anterior)/self.dt
        u = self.Kp*erro + self.Kd*derivada
        self.erro_anterior = erro
        return u

    def reset(self):
        # zera o erro anterior
        self.erro_anterior = 0