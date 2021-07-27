#!/bin/bash
git clone https://github.com/ahmdrz/telegram-prober temp
mv temp/helm-chart telegram-prober
rm -rf temp
helm package telegram-prober
rm -rf telegram-prober
helm repo index .
