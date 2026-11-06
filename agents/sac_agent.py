# O que faz esse código?

import onnxruntime as ort
import numpy as np

class SACAgent:
    def __init__(self, model_path, gain = 3*np.pi/4):
        self.sess = ort.InferenceSession(model_path)
        self.input_name = self.sess.get_inputs()[0].name
        self.gain = gain

    def get_action(self, obs):
        obs = np.array(obs, dtype=np.float32).reshape(1, -1)
        outputs = self.sess.run(None, {self.input_name: obs})
        mean = outputs[0].flatten()[0] #ignora outputs[1] (std) na inferência
        return self.gain * np.tanh(mean)