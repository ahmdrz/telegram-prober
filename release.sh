#!/bin/bash
git clone https://github.com/ahmdrz/telegram-prober
mv telegram-prober/helm-chart .
rm -rf telegram-prober
zip -r telegram-prober.zip helm-chart
rm -rf helm-chart
