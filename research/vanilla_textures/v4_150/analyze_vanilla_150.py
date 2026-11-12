#!/usr/bin/env python3
"""Recompute all 150 pixel metrics from user-owned 1.21.11 Minecraft assets.
The input must be either a full client.jar or an extracted block PNG directory.
"""
import analyze_vanilla_100 as base
from pathlib import Path
import csv
from argparse import ArgumentParser

ROOT=Path(__file__).resolve().parent
with (ROOT/'02_신규50종_SHA256_출처.csv').open(encoding='utf-8-sig',newline='') as f:
    extra=list(csv.DictReader(f))
for row in extra:
    base.LABELS[row['texture_id']]=row['group']
    base.FAMILIES.setdefault(row['group'],[]).append(row['texture_id'])
base.run()
