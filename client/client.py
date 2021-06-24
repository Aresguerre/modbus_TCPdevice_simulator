import sunspec2.modbus.client as client
import sunspec2.mb as utils

regs =[{
    "name" : "Operation.health",
    "reg_addr" : 30201,
    "reg_count" : 1,
    "type" : "enum",
    "map" : {35:"Fault", 303:"Off", 307:"Ok", 455:"Warning"}
},
{
    "name" : "Metering.TotWhOut",
    "reg_addr" : 30513,
    "reg_count" : 4,
    "type" : "uint"
},
{
    "name" : "Metering.DyWhOut",
    "reg_addr" : 30535,
    "reg_count" : 2,
    "type" : "uint"
},
{
    "name" : "GridMs.TotW",
    "reg_addr" : 30775,
    "reg_count" : 2,
    "type" : "int"
},
{
    "name" : "Env.TmpVal",
    "reg_addr" : 34609,
    "reg_count" : 2,
    "type" : "int"
},
{
    "name" : "Env.HorWSpd",
    "reg_addr" : 34615,
    "reg_count" : 2,
    "type" : "uint"
}]
def read_registers(d, name):
    register = next((x for x in regs if x['name'] == name), None)
    print("reading register ", name, " on address ", register['reg_addr'])
    value = 0
    
    if register['reg_count']==4:
        if register['type']=="int":
            value = utils.data_to_s64(d.read(register['reg_addr'],4))
        elif register['type']=="uint":
            value = utils.data_to_u64(d.read(register['reg_addr'],4))
    
    if register['reg_count']==2:
        if register['type']=="int":
            value = utils.data_to_s32(d.read(register['reg_addr'],2))
        elif register['type']=="uint":
            value = utils.data_to_u32(d.read(register['reg_addr'],2))

    if register['reg_count']==1:
        if register['type']=="int":
            value = utils.data_to_s16(d.read(register['reg_addr'],1))
        elif register['type']=="uint":
            value = utils.data_to_u16(d.read(register['reg_addr'],1))
        elif register['type']=="enum":
            intVal = utils.data_to_u16(d.read(register['reg_addr'],1))
            value = register['map'][intVal]
    
    print(register['name'], value)



def read_mesurements(client):
    print("reading mesurements...")
    read_registers(client, 'Operation.health')

if __name__=='__main__':
    d = client.SunSpecModbusClientDeviceTCP(slave_id=1, ipaddr='127.0.0.1', ipport=8502)

    d.scan()
    read_mesurements(d)
    # print(d.models)
    # print(utils.data_to_u64(d.read(30513, 4)))

    # d.write(30513, utils.u64_to_data(2))
    # print(utils.data_to_u64(d.read(30513, 4)))