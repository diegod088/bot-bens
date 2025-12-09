#!/usr/bin/env bash
set -e

echo "===== PYTHON VERSION ====="
python --version

echo "===== INSTALLED PTB ====="
pip show python-telegram-bot || true

echo "===== CLEANING CACHE ====="
find . -name "*.pyc" -delete || true
find . -type d -name "__pycache__" -exec rm -rf {} + || true

echo "===== STARTING BOT ====="
python bot_with_paywall.py
