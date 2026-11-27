import psutil

def get_disk_usage():
    disk_stat = psutil.disk_usage('/')
    return {
        "total": disk_stat.total,
        "used": disk_stat.used,
        "free": disk_stat.free,
        "percent": disk_stat.percent,
    }