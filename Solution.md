## Minimal E-commerce Backend API Development Test Solution

### Setup 

- Install dependencies
```sh
poetry install
```

- Activate poetry venv 
```sh
poetry shell
```
- Run makemigrations (This is because dev migrations are not being pushed to Github)
```sh
make mms
```

- Run Migrate
```sh
make migrate
```

- Start the application
```sh
make run
```

- Visit Postman Documentation
[docs](https://documenter.getpostman.com/view/35174244/2sA3kVjgC9)

- Run Test
```sh
make test
```




