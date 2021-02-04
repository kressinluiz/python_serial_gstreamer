import asyncio
import serial_asyncio


class Output(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        transport.write(b'Hello, World!\n')  # Write serial data via transport

    def data_received(self, data):
        print('data received', data)

    #        if b'\n' in data:
    #            self.transport.write(b'Hello, World!\n')
    #            self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')


# https://docs.python.org/3/library/asyncio-eventloop.html
# asyncio.get_event_loop() :
# Function: get the current event loop OR create a new event loop and set it as the current one
# IF there is no current event loop set in the current OS thread,
# AND set_event_loop() has not yet been called
# THEN asyncio will create a new event loop and set it as the current one
loop = asyncio.get_event_loop()

# serial_asyncio.create_serial_connection(loop, protocol_factory, *args, **kwargs)
#   Function: Get a connection making coroutine
# Parameters:
#           loop - The event handler
#           protocol_factory - Factory function(asyncio.coroutine) for a asyncio.Protocol
#           args, kwargs - Passed to the serial.Serial init function
coro = serial_asyncio.create_serial_connection(loop, Output, '/dev/ttyAMA0', baudrate=2000000)

# loop.run_until_complete(future)
# Function: run until the future(an instance of Future) has completed
#           If the argument is a coroutine object it is implicitly scheduled to run as a asyncio.Task
loop.run_until_complete(coro)

loop.run_forever()
loop.close()
