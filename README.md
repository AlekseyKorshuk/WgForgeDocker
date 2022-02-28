# WGForge Docker Home Work

## How to use

```shell
git clone https://github.com/AlekseyKorshuk/WgForgeDocker
cd WgForgeDocker
docker-compose up --build
```

Change PostgreSQL platform in _docker-compose.yalm_:

```yaml
  db:
    platform: linux/x86_64
    image: postgres
```

Build container:

```shell
docker-compose up --build
```

