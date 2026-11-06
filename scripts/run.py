from core.loop import ControlLoop
import os

if __name__ == "__main__":
    
    os.system("PYTHONPATH=. python3 scripts/calibrate.py") # o que este método faz?
    loop = ControlLoop()
    loop.start()
    