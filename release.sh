#!/bin/bash

set -e

git clone https://github.com/ahmdrz/telegram-prober temp
mv temp/helm-chart telegram-prober
rm -rf temp
helm package telegram-prober --version $HELM_VERSION
rm -rf telegram-prober
helm repo index . --url https://ahmdrz.github.io/telegram-prober
