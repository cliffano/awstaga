#!/usr/bin/env bash
set -o nounset

export AWS_DEFAULT_REGION=ap-southeast-2

echo "\n\n========================================"
echo "Show help guide: awstaga --help"
awstaga --help

echo "\n\n========================================"
echo "Run command with default config file: awstaga"
awstaga

echo "\n\n========================================"
echo "Run command with specified config file:"
echo "awstaga --conf-file awstaga.yaml"
awstaga --conf-file awstaga.yaml

echo "\n\n========================================"
echo "Run command with specified config file and AWS_DEFAULT_REGION env var:"
echo "AWS_DEFAULT_REGION=ap-southeast-2 awstaga --conf-file awstaga.yaml"
awstaga --conf-file awstaga.yaml

echo "\n\n========================================"
echo "Run command with specified config file in dry-run mode:"
echo "awstaga --conf-file awstaga.yaml --dry-run"
awstaga --conf-file awstaga.yaml --dry-run

echo "\n\n========================================"
echo "Run command with specified config file in dry-run mode with custom batch size:"
echo "awstaga --conf-file awstaga.yaml --dry-run"
awstaga --conf-file awstaga.yaml --dry-run --batch-size 50
