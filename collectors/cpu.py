import psutil

def get_cpu_usage():
    cpu_stat = psutil.cpu_stats()
    return {
        "usage": psutil.cpu_percent(interval=1),
        "frequency": psutil.cpu_freq().current
        if psutil.cpu_freq() is not None else None,
    }