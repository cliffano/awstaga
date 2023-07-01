#!/bin/sh

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
AWS_DEFAULT_REGION=ap-southeast-2 awstaga --conf-file awstaga.yaml