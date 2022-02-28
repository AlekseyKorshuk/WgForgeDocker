# WGForge Docker Home Work

## How to use

```shell
git clone 
cd 
docker-compose up --build
```

Change PostgreSQL platform in _docker-compose.yalm_:

```shell
  db:
    platform: linux/x86_64
    image: postgres
```

Build container:

```shell
docker-compose up --build
```

