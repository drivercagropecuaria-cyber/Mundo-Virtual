#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Runner para STAGE4_EXECUTOR_WINDOWS com credenciais definidas
"""
import os
import subprocess
import sys

# Define environment variables directly in Python
os.environ['DB_HOST'] = 'host.docker.internal'
os.environ['DB_PORT'] = '5432'
os.environ['DB_NAME'] = 'BIBLIOTECA'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'postgres'

# Run the executor
result = subprocess.call([sys.executable, 'STAGE4_EXECUTOR_WINDOWS.py'])
sys.exit(result)
