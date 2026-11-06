import inspect_onnx
import onnxruntime as ort
import numpy as np
from agents.sac_agent import SACAgent

sac = SACAgent("agents/weights/sac_actor_swingup.onnx", action_low = 0.0, action_high=np.pi)
