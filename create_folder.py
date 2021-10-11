#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

try: 
    os.mkdir("/home/zavecz/final/soccer/analysis/temp")
    os.mkdir("/home/zavecz/final/soccer/analysis/output")
except OSError as error: 
    pass