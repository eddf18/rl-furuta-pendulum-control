import pigpio

class QUBEMotor:
    def __init__(self, pi, pwm_pin, dir_pin, brake_pin, frequency):
        self._pwm_pin = pwm_pin
        self._dir_pin = dir_pin
        self._brake_pin = brake_pin
        self._frequency = frequency
        self.pi = pi

        pi.set_mode(dir_pin, pigpio.OUTPUT)
        pi.set_mode(brake_pin, pigpio.OUTPUT)

        pi.set_PWM_frequency(pwm_pin, frequency)
        pi.set_PWM_range(pwm_pin, 1000) # 0 - 1000 = 0 - 100%

        pi.write(brake_pin, pigpio.LOW)


    def set_voltage(self, voltage, max_voltage):
        _voltage = max(-max_voltage, min(voltage,max_voltage))
        if (_voltage > 0):
            self.pi.write(self._dir_pin, 1)
        else:
            self.pi.write(self._dir_pin, 0)

        duty = int(abs(_voltage)/max_voltage * 1000)
        self.pi.set_PWM_dutycycle(self._pwm_pin, duty)
    
    def brake(self):
        self.pi.write(self._brake_pin, 1)
        self.stop()

    def release_brake(self):
        self.pi.write(self._brake_pin, 0)

    def stop(self):
        self.pi.set_PWM_dutycycle(self._pwm_pin, 0)

    def shutdown(self):
        self.stop()
        self.brake()
        self.pi.stop()