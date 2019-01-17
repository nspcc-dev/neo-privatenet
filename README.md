# Private network for NEO blockchain testing

Based on [CityOfZion container](https://github.com/CityOfZion/neo-privatenet-docker)

## How to boot up environment

You can run `make up` (`make privnet`) to run environment.

## What inside?

Inside we run:
- 4 Neo consensus nodes
- Mechanism of auto import smart contract
- NeoScan API
- PostgreSQL

## Logs

Consensus nodes run in `GNU/screen` and send their logs to docker-log

Mechanism of import smart contract is waiting for ENV-variables

You can follow logs to see process of SC import by `make logs`

## Environment file

*System*
- TZ - System default time

*Smart contract*
- CONTRACT_ARGS - arguments to deploy smart-contract
- CONTRACT_FILE - path to smart-contract file in container
- CONTRACT_FILE_LOCAL - path to local smart-contract file

*Postgres*
- POSTGRES_USER - username for PostgreSQL database 
- POSTGRES_HOSTNAME - hostname for PostgreSQL database 
- POSTGRES_PASSWORD - password for PostgreSQL database
- POSTGRES_DATABASE - default database for PostgreSQL database 

*NEO Scan*
- NEO_SEED_{NUM:1-4} - host for neo-scan synchronization

## Makefile
```
  Usage:

    make <target>

  Targets:

    down      Stop private-net environment
    help      Show this help prompt
    kill      Kill private-net environment
    logs      Follow containers logs
    privnet   Run only private-net without neo-scanner and postgresql
    up        Up private-net full environment
```

# Contributing

At this moment, we do not accept contributions. Follow us.

## License

This project is licensed under the GPL v3.0 License - see the 
[LICENSE](LICENSE) file for details