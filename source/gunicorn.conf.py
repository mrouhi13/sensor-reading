"""Gunicorn configuration file."""
import multiprocessing

bind = '0.0.0.0:8000'
chdir = '.'
workers = multiprocessing.cpu_count() * 2 + 1
max_requests = 2000
max_requests_jitter = 400
preload = True
log_file = None
access_logfile = None
error_logfile = None
log_level = 'warning'
worker_tmp_dir = '/dev/shm'
