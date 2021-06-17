Building and running container

```
git clone https://github.com/Aresguerre/modbus_TCPdevice_simulator.git

docker build -t device_sim

docker run -it -p 8502:8502 device_sim
```

Testing against sunspec2 client

```
pipenv install pysunspec2

pipenv install pyserial

pipenv shell

python

import sunspec2.modbus.client as client

d=client.SunSpecModbusClientDeviceTCP(slave_id=1, ipaddr='127.0.0.1', ipport=8502)

d.scan()

d.common[0].read()

d.common[0].Mn.value

```
