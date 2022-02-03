## Python, JS, & React | Build a Blockchain & Cryptocurrency

#### Command Reference

**Activate the Docker virtual environment**

```
docker-compose up bc
```

**Install all packages**

```
pip3 install -r requirements.txt
```

**Run the tests**

Make sure to activate the virtual environment.

```
./be/run_tests
```

**Run the application and API**

Make sure to activate the virtual environment.

```
./be/run_flask_debug
```

**Run a peer instance**

Make sure to activate the virtual environment.

```
./be/run_flask_peer
```

**Run the frontend**

In the frontend directory:

```
npm run start
```

**Seed the backend with data**

Make sure to activate the virtual environment.

```
export SEED_DATA=True && python3 -m backend.app
```
