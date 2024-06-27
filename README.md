# Scraper Bot

[![GitHub](https://img.shields.io/github/license/RobertoBochet/scraper-bot?style=flat-square)](https://github.com/RobertoBochet/scraper-bot)
[![GitHub Version](https://img.shields.io/github/v/tag/RobertoBochet/scraper-bot?label=version&style=flat-square)](https://github.com/RobertoBochet/scraper-bot)
[![PyPI - Version](https://img.shields.io/pypi/v/scraper-bot)](https://pypi.org/project/scraper-bot/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/RobertoBochet/scraper-bot/test-code.yml?label=test%20code&style=flat-square)](https://github.com/RobertoBochet/scraper-bot)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/RobertoBochet/scraper-bot/release.yml?label=publish%20release&style=flat-square)](https://github.com/RobertoBochet/scraper-bot/pkgs/container/scraper-bot)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/RobertoBochet/scraper-bot?style=flat-square)](https://www.codefactor.io/repository/github/robertobochet/scraper-bot)

This is a bot thought to do periodical scraping of ads from commercial websites.

Found a new ad the bot will send it to you exploiting [Apprise](https://github.com/caronc/apprise) channels

## Deploy

### Pypi

The relative package is available on [Pypi](https://pypi.org/project/scraper-bot/)

```shell
pipx install scraper-bot
```
The package provide the following command
```shell
scraper-bot
```

### Container

The CI builds the container for each version and it puts it on the public [GitHub registry](https://ghcr.io/robertobochet/scraper-bot)
```
ghcr.io/robertobochet/scraper-bot
```

#### docker compose

1. [Create a telegram bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot) and retrieve its token
2. Download `config.example.yaml` and rename it to `config.yaml`
3. Change the configuration follow the [guidelines](#configuration)
4. Download `docker-compose.yaml`
5. Start the scraper with `docker-compose`
    ```shell
    docker-compose up
    ```
6. Wait that the bot does its work!

### Kubernetes (Helm chart)

For the deploy of the **Scraper Bot** is also available a [helm chart](https://helm.sh/)

You can found the source code in the repo [`scraper-bot-chart`](https://github.com/RobertoBochet/scraper-bot-chart)

Helm chart package is available in the github OCI registry
```
oci://ghcr.io/robertobochet/scraper-bot-chart
```
You can use it to directly deploy on your kubernetes cluster
1. Retrieve the default values file
   ```shell
   helm show values oci://ghcr.io/robertobochet/scraper-bot-chart > values.yaml
   ```
2. Customize the `values.yaml`
3. Install the scaper bot
   ```shell
   helm install oci://ghcr.io/robertobochet/scraper-bot-chart scraper-bot -f values.yaml
   ```

## Configuration

By default the bot looks for a configuration file in the following path `./config.y(a)ml` and `/etc/scaraper-bot/config.y(a)ml`. You cna override this behavior passing via command line the `--config` argument followed by the config file path
```shell
scraper-bot --config /path/to/scraper-bot-config.yaml
```

The configuration file has to satisfy the pydantic model which you can find in `scraper_bot.settings`.
Furthermore you can get the config json schema from command line with `--config-schema` argument
```shell
scraper-bot --config-schema
```

You can also find a configuration example in `config.example.yaml`.
