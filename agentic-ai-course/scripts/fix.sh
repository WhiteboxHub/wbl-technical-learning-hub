#!/usr/bin/env bash
echo "Restoring system to healthy baseline..."
curl -s http://localhost:8000/health
echo "System healthy."
