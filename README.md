Building and running container

```
git clone https://github.com/Aresguerre/modbus_TCPdevice_simulator.git

docker build -t device_sim .

docker run -p 8502:8502 device_sim
```

Testing against sunspec2 client

```
pipenv install pysunspec2

pipenv shell

python3 client/client.py
```
