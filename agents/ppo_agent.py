import onnxruntime as ort
import numpy as np

class PPOAgent:
    def __init__(self, model_path):
        self.sess = ort.InferenceSession(model_path)
        self.input_name = self.sess.get_inputs()[0].name

    def get_action(self, obs):
        obs = np.array(obs, dtype=np.float32).reshape(1, -1)
        probs = self.sess.run(None, {self.input_name: obs})[0].flatten()
        return int(np.argmax(probs))