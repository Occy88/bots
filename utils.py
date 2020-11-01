import numpy as np
import psutil


def get_process_by_name(name):
    processes = psutil.process_iter()
    for p in processes:
        try:
            process_name = p.name()
            pid = p.pid
            if process_name == name:
                return p
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

