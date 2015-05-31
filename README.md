Before running app make sure you have **python** and **pip** installed.

To install dependencies run:
```
pip install -r requirements
```
You can either install it inside virtualenv or globally.
If installing globally you need to run it as root.

Project can be run as regular flask app in dev mode:
```
python dashboard.py
```

or using twisted which is WSGI container and supports more threads than "dev mode".
```
twistd -n web --port 8080 --wsgi dashboard.app
```
