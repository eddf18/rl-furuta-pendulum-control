# Script para fazer a leitura dos encoders

import pigpio
import math


class QuadratureEncoder:

    _TRANSITION = [
         0, -1, +1,  0,
        +1,  0,  0, -1,
        -1,  0,  0, +1,
         0, +1, -1,  0,
    ]

    def __init__(self, pi, pin_a, pin_b, ppr):
        self.pi          = pi
        self.pin_a       = pin_a
        self.pin_b       = pin_b
        self.ppr         = ppr
        self._count      = 0
        self._last_state = 0

        pi.set_mode(pin_a, pigpio.INPUT)
        pi.set_mode(pin_b, pigpio.INPUT)
        pi.set_pull_up_down(pin_a, pigpio.PUD_UP)
        pi.set_pull_up_down(pin_b, pigpio.PUD_UP)

        a = pi.read(pin_a)
        b = pi.read(pin_b)
        self._last_state = (a << 1) | b

        self._cba_a = pi.callback(self.pin_a, pigpio.EITHER_EDGE, self._update)
        self._cba_b = pi.callback(self.pin_b, pigpio.EITHER_EDGE, self._update)

    def _update(self, gpio, level, tick):
        a     = self.pi.read(self.pin_a)
        b     = self.pi.read(self.pin_b)
        state = (a << 1) | b
        idx   = (self._last_state << 2) | state
        self._count     += self._TRANSITION[idx]
        self._last_state = state

    def reset(self):
        self._count      = 0
        self._last_state = 0

    @property
    def count(self):
        return self._count

    @property
    def angle_rad(self):
        return (self._count / (self.ppr * 4)) * 2 * math.pi

    def cancel(self):
        self._cba_a.cancel()
        self._cba_b.cancel()