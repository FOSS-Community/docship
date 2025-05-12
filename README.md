<p align="center">
    <img src="./artwork/dockership-logo.png" width="10%" />
    <h1 align="center">docship ⛴️</h1>
    <h3 align="center">A tool to deploy stuff running on docker</h3>
</p>

## Installation

Install docship with pip

```bash
  pip3 install docship

  docship --version
```

Install from source

```bash
  git clone https://github.com/foSS-Community/docship

  cd docship

  python3 -m pip3 install .

  docship --version
```

## Usage

```
docship --help
usage: docship [-h] [--version] {deploy} ...

Dockership CLI for managing deployments.

options:
  -h, --help     show this help message and exit
  --version, -v  to get the current version of docship

Commands:
  {deploy}       Available commands
    deploy       Deploy an application to a server
```

### To deploy a site running in docker or any port
```
usage: docship deploy [-h] --name NAME --address ADDRESS

options:
  -h, --help            show this help message and exit
  --name, -n NAME       The name of the server where the application will be deployed, ex.
                        api.example.com
  --address, -a ADDRESS
                        The address of the application server, ex. http://localhost:8000
```

```
docship deploy -n xyz.fosscu.org -a http://localhost:8082
```

## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.

## Authors

- [@Mr-Sunglasses](https://www.github.com/Mr-Sunglasses)

## License

[MIT](https://choosealicense.com/licenses/mit/)

## 💪 Thanks to all Wonderful Contributors

Thanks a lot for spending your time helping AutoType grow.
Thanks a lot! Keep rocking 🍻

## 🙏 Support++

This project needs your shiny star ⭐.
Don't forget to leave a star ⭐️

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
