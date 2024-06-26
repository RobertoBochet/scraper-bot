# Scraper Bot

[![GitHub](https://img.shields.io/github/license/RobertoBochet/scraper-bot?style=flat-square)](https://github.com/RobertoBochet/scraper-bot)
[![GitHub Version](https://img.shields.io/github/v/tag/RobertoBochet/scraper-bot?label=version&style=flat-square)](https://github.com/RobertoBochet/scraper-bot)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/RobertoBochet/scraper-bot/test-code.yml?label=test%20code&style=flat-square)](https://github.com/RobertoBochet/scraper-bot)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/RobertoBochet/scraper-bot/build-container.yml?label=build%20container&style=flat-square)](https://github.com/RobertoBochet/scraper-bot/pkgs/container/scraper-bot)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/RobertoBochet/scraper-bot?style=flat-square)](https://www.codefactor.io/repository/github/robertobochet/scraper-bot)

This is a bot thought to do periodical scraping of ads from commercial websites.

Found a new ad the bot will send it to you exploiting [Apprise](https://github.com/caronc/apprise) channels

## Deploy

The CI builds the container for each version and, it puts it on the public [GitHub registry](https://ghcr.io/robertobochet/scraper-bot)
```
ghcr.io/robertobochet/scraper-bot
```

As alternative, you can build by yourself the python package or the container

### Fast deploy (docker-compose)

1. [Create a telegram bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot) and retrieve its token
2. Download `config.example.yaml` and rename it to `config.yaml`
3. Change the configuration follow the [guidelines](#configuration)
4. Download `docker-compose.yaml`
5. Start the scraper with `docker-compose`
    ```bash
    docker-compose up
    ```
6. Wait that the bot does its work!

## Configuration

By default the bot looks for a configuration file in the following path `./config.y(a)ml` and `/etc/scaraper-bot/config.y(a)ml`. You cna override this behavior passing via command line the `--config` argument followed by the config file path
```bash
scraper_bot --config /path/to/scraper-bot-config.yaml
```

The configuration file has to satisfy the pydantic model which you can find in `scraper_bot.settings`.
Furthermore you can get the config json schema from command line with `--config-schema` argument
```bash
scraper_bot --config-schema
```

You can also find a configuration example in `config.example.yaml`.
