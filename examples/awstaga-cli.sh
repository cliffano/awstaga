#!/usr/bin/env bash
set -o nounset

export AWS_DEFAULT_REGION=ap-southeast-2

printf "\n\n========================================\n"
printf "Show help guide: awstaga --help\n"
awstaga --help

printf "\n\n========================================\n"
printf "Run command with default config file: awstaga\n"
awstaga

printf "\n\n========================================\n"
printf "Run command with specified config file:\n"
awstaga --conf-file awstaga.yaml

printf "\n\n========================================\n"
printf "Run command with specified config file and AWS_DEFAULT_REGION env var:\n"
awstaga --conf-file awstaga.yaml

printf "\n\n========================================\n"
printf "Run command with specified config file in dry-run mode:\n"
awstaga --conf-file awstaga.yaml --dry-run

printf "\n\n========================================\n"
printf "Run command with specified config file in dry-run mode with custom batch size:\n"
awstaga --conf-file awstaga.yaml --dry-run --batch-size 50
