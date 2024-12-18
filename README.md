<div align="center">
<div><img src=".github/images/cws.png" width="312" alt="cws2"></div>

**cws2**, or **conworkshop 2**, is a website to bring conlangers together.

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/m5ka/cws2/test.yaml?label=tests)
![GitHub contributors](https://img.shields.io/github/contributors/m5ka/cws2)
![Python version: >= 3.12](https://img.shields.io/badge/python-%3E%3D%203.12-blue?logo=python&logoColor=white)
[![Django version 5.1](https://img.shields.io/badge/django-5.1-green?logo=django)](https://docs.djangoproject.com/en/5.1/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
</div>

## 🐻 About
This project is the [Django](https://www.djangoproject.com/) successor to the original PHP ConWorkShop. It aims to be a modern, stable and more future-proof version of the site whilst maintaining the spirit of ConWorkShop's vibrant past and community.

## 🏄 Setup
### Requirements
* Python (3.12 or above)
* Poetry
* PostgreSQL

### Setting up
Once you've cloned the repo, you'll need to make sure your Python environment has everything it needs to run cws2. You can do that with Pip.

It's worth using a Python [virtual environment](https://docs.python.org/3/tutorial/venv.html) to keep everything clean. We recommend using [pyenv](https://github.com/pyenv/pyenv) alongside [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to manage this.

To install all the packages to Pip that you'll need for cws2 as well as for local development and testing, just run:
```bash
poetry install --with dev,test
```

### Configuring
Now you're all installed, there's a few things you'll want to do before your first run.
```bash
make env
```
This will set you up a `.env` file, which you should edit to update your configuration.

Make sure you fill in `DATABASE_URL` as it's used to connect to your database. The format is `postgres://user:password@host:port/database`. Also ensure that the Postgres user has the Create DB permission, or you might get an error when trying to run tests.

Once you've finished configuring your environment, you can migrate the database using:
```bash
make migrate
```

### Run the server
Finally you should be able to run the server. Woohoo! 🎉
```bash
make serve
```

If you'd like to access the development site on other devices on your local network, you should launch with the command `make servelan` instead. Just make sure you add the server device's local IP to the `ALLOWED_HOSTS` environment setting when configuring otherwise local network devices won't be allowed to connect.

## 📌 Deploying
### Server
For production, ensure `SECRET_KEY` and `ALLOWED_HOSTS` are set correctly! These are very important for security. `DEBUG` should also be set to false.

If you're happy with everything and are ready to launch an instance of cws2 into production, you can do this via Gunicorn. With all the project dependencies already set up, you can launch the server with the following command. (Adjust certain parameters to you and your server's needs!)

```bash
gunicorn --access-logfile - --workers 3 cws2.config.wsgi:application
```

You can use the `--bind` parameter to bind the server to a specific socket, which can be useful for certain server management setups e.g controlling it with systemd.

### Assets
When running the production server, you will have to serve static assets yourself! This is most easily done with a server like Nginx, which can also be used to proxy requests to the Gunicorn server/socket.

In development, the Django server automatically fetches the static files of any dependencies but the production server won't know where these are so you'll need to manually collect up all the static files of any dependencies into your project environment. Luckily there's a management command for this.

```bash
make static
```

## 🤖 Development
### 🎨 Compiling Assets
Style assets are written in SASS and compiled on the server, so when developing locally you need to make sure you compile these assets before you see any change on your development copy. You can do that with:
```bash
make sass
```

Alternatively, to compile assets and keep watching for new changes, you can run:
```bash
make watch
```

### 🧪 Testing
We use [pytest](https://docs.pytest.org/en/7.2.x/) for testing. You can run tests with the following command:
```bash
make test
```

### 🧩 Migrations

If you make any changes to models, you'll need to write migrations so that users of the app can keep their database up to date with these changes.

Migrations are written as regular Python scripts in the `cws2/migrations` directory, and you can read about how to write them [here](https://docs.djangoproject.com/en/4.1/topics/migrations/).

There's a script for auto-generating migrations based on changes you make to models which you can run using the command below:
```bash
make migrations
```

Note that for more complex changes such as modifying data in the database, you'll have to write the migration yourself. You can generate a blank migration file using the following command.

```bash
python manage.py makemigrations cws2 --empty -n my_migration
```

### 🍓 Code style
We care about code style, so all code should be compliant with [ruff](https://docs.astral.sh/ruff/)'s formatter and linter.

You can check whether your code is compliant with the above using the following command.
```bash
make lint
```

You can also automatically format your code with the following command.

```bash
make format
```

Code editors often have tools to automate this, such as in [VS Code](https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0).

## 🤝 Contributing
We'd love for you to contribute! Read [CONTRIBUTING.md](CONTRIBUTING.md) for some guidelines, and keep in mind our style guidelines. Also, make sure you follow our [code of conduct](CODE_OF_CONDUCT.md) when contributing on GitHub.

## 📚 License
cws2 is licensed under a [BSD 2-Clause](https://opensource.org/licenses/BSD-2-Clause) license - see [LICENSE](LICENSE) to read it in full.

## 🌳 Acknowledgements
Thanks to Jay (hashi) for all your hard work on CWS's first version. We love you. 💘
