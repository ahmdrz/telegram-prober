# Telegram Prober
---
> A simple prober in order to monitor your telegram bots.


### Configuration

First, you have to create an application in Telegram. Read [Creating your Telegram Application](https://core.telegram.org/api/obtaining_api_id) on the Telegram website. Then put values in app environment. You can also store environment variables in `.env` file.

```
export TELEGRAM_API_ID='<telegram api_id>'
export TELEGRAM_API_HASH='<telegram api_hash>'
```

You need some telegram sessions to communicate with other telegram bots. In other to get telegram session follow 
the steps blow:

```
python save_session.py <phone_number: with country code, ex: '+98912...'> 
```

**Note**: You can use multiple sessions to avoid blocking by the Telegram rate-limiter.

Store sessions like a CSV format in `TELETHON_SESSIONS` variable:

```
export TELETHON_SESSIONS='<session one>,<session two>,...'
```

### Helm Chart

To use the Helm Chart, you have to configure variables in `values.yaml` file. For example look at the `values.yaml` 
in `helm-chart` directory.

You should update `telegramAccountConfig` and `prober.targets`.

```
helm repo add telegram-prober https://ahmdrz.github.io/telegram-prober
helm install telegram-prober --values values.yaml 
```
