#!/usr/bin/env python

import sys
import struct
import socket
import modbus_tk
import modbus_tk.modbus_tcp as modbus_tcp
from simulator import *
import mbmap
from optparse import OptionParser
from math import floor


class ModSimError(Exception):
    pass

class ModSimDatabank(modbus_tk.modbus.Databank):

    def handle_request(self, query, request):
        """
        when a request is received, handle it and returns the response pdu
        """
        request_pdu = ""
        try:
            #extract the pdu and the slave id
            (slave_id, request_pdu) = query.parse_request(request)

            #get the slave and let him executes the action
            if slave_id == 0:
                #broadcast
                for key in self._slaves:
                    self._slaves[key].handle_request(request_pdu, broadcast=True)
                return
            else:
                slave = self.get_slave(slave_id)
                response_pdu = slave.handle_request(request_pdu)
                #make the full response
                response = query.build_response(response_pdu)
                return response
        except Exception as excpt:
            modbus_tk.hooks.call_hooks("modbus.Databank.on_error", (self, excpt, request_pdu))
            LOGGER.error("handle request failed: " + str(excpt))
        except:
            LOGGER.error("handle request failed: unknown error")

        #If the request was not handled correctly, return a server error response
        ''' ### don't send response on error
        func_code = 1
        if len(request_pdu) > 0:
            (func_code, ) = struct.unpack(">B", request_pdu[0])
        return struct.pack(">BB", func_code+0x80, defines.SLAVE_DEVICE_FAILURE)
        '''

class ModSim(Simulator):
    def __init__(self, options):
        self.rtu = None
        self.mode = options.mode

        if options.mode == 'tcp':
            Simulator.__init__(self, modbus_tcp.TcpServer(address = '', port = options.port))
        else:
            raise ModSimError('Unknown mode: %s' % (options.mode))

        self.server.set_verbose(options.verbose)


if __name__ == "__main__":

    usage = 'usage: %prog [options] map_file'
    parser = OptionParser(usage=usage)
    parser.add_option('-m', '--mode',
                      default='tcp',
                      help='mode: rtu, tcp [default: rtu]')
    parser.add_option('-p', '--port', type='int',
                      default=502,
                      help='IP port [default: 502]')
    parser.add_option('-i', '--id', type='int',
                      default=1,
                      help='slave id [default: 1]')
    parser.add_option('-v', '--verbose', type='int',
                      default=0,
                      help='verbose: 0 or 1 [default: 0]')

    options, args = parser.parse_args()

    if len(args) != 1:
        print(parser.print_help())
        sys.exit(1)

    modbus_map = mbmap.ModbusMap(options.id)
    try:
        map_name = args[0]
        ext = os.path.splitext(map_name)[1]
        modbus_map.from_xml(map_name)
    except IOError as e:
        print('Error loading modbus map file - %s' % (str(e)))
        sys.exit(1)

    # create simulator
    try:
        sim = ModSim(options)
    except ModSimError as e:
        print('Error initializing the simulator - %s' % (str(e)))
        sys.exit(1)

    if sim.mode == 'tcp':
        print('Initialized modbus %s simulator: addr = %s  port = %s  slave id = %s  base address = %s' % (options.mode,socket.gethostbyname('localhost'), options.port, str(options.id), str(modbus_map.base_addr)))
    else:
        print('Initialized modbus simulator to unknown mode: %s' % (sim.mode))
    
    # add modbus map to simulator slave device
    print('Modbus map loaded from %s' % args[0])
    slave = sim.server.add_slave(options.id)
    for regs in modbus_map.regs:
        print(regs.offset)
        slave.add_block('regs_' + str(regs.offset), modbus_map.func, (modbus_map.base_addr + regs.offset), int(regs.count))
    for regs in modbus_map.regs:
        values = []
        print(regs.count)
        for i in range(0, int(floor(regs.count))):
            index = i * 2
            v = struct.unpack('>H', regs.data[index:(index + 2)])
            values.append(v[0])
        # print values
        slave.set_values('regs_' + str(regs.offset), (modbus_map.base_addr + regs.offset), values)
        #print(slave)
        print('Added modbus map block:  address = %d  count = %d' % ((modbus_map.base_addr + regs.offset), regs.count))

    try:
        LOGGER.info("'quit' for closing the simulator")
        sim.start()

    except Exception as e:
        print(e)
            
    finally:
        sim.close()

