Building and running container

```
git clone -b feature/modbus_server_new_data https://github.com/Aresguerre/modbus_TCPdevice_simulator.git

docker build -t device_sim:latest .

docker run -p 8502:8502 -it device_sim:latest
```

Testing against sunspec2 client

```
pipenv install pysunspec2

pipenv shell

python3 client/client.py
```
