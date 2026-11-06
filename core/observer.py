# Script para produzir o vetor de estados

import math

class Observer:

    def __init__(self, enc_arm, enc_pendulum, dt):
        self._enc_arm = enc_arm
        self._enc_pendulum = enc_pendulum
        self.dt = dt
        self._phi_anterior = 0
        self._theta_anterior = 0

    def update(self):
        # leitura dos encoders com base nos outros arquivos
        self._phi = self._enc_pendulum.angle_rad
        self._theta = self._enc_arm.angle_rad

        #calculo das velocidades
        self._omega_theta = (self._theta - self._theta_anterior) / self.dt
        self._omega_phi = (self._phi - self._phi_anterior) / self.dt

        # atualiza os anteriores
        self._theta_anterior = self._theta
        self._phi_anterior = self._phi

    @property
    def theta(self):
        return self._theta
    
    @property
    def phi(self):
        return self._phi
    
    @property
    def omega_theta(self):
        return self._omega_theta
    
    @property
    def omega_phi(self):
        return self._omega_phi
    
    # aqui eu preciso retornar os senos e cossenos dos ângulos
    @property
    def observation(self):
        return [
            math.sin(self._theta),
            math.cos(self._theta),
            math.sin(self._phi),
            math.cos(self._phi),
            self._omega_theta,
            self._omega_phi
        ]