import psutil

def get_ram_usage():
    ram_stat = psutil.virtual_memory()
    return {
        "total": ram_stat.total,
        "used": ram_stat.used,
        "free": ram_stat.free,
        "percent": ram_stat.percent,
    }