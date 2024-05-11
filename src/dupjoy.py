import socket
import time
import src.event_utils as event_utils
import pyvjoy
import threading

class DupjoyClient:
    """
    Dupjoy Client will read controller events and send them to server (if provided)
    """

    def __init__(self, server_ip, server_port):
        import pygame # server does not need pygame so import here
        self.pygame = pygame

        self.server_ip = server_ip
        self.server_port = server_port
    
    def start(self):
        self.exiting = False
        self.__init_keypress()

        self.pygame.init()
        self.pygame.joystick.init()
        self.__init_joystick()
        self.vjoy = pyvjoy.VJoyDevice(1)
        
        self.local_on = True
        self.remote_on = True
        self.socket = None
        self.server_connection_thread = threading.Thread(target=self.__server_connection_procedure)
        self.server_connection_thread.start()

        # genshin autoclick
        self.gi_dialog_auto_click = False
        self.gi_dialog_auto_click_thread = threading.Thread(target=self.__gi_dialog_auto_click_procedure)
        self.gi_dialog_auto_click_thread.start()

        try:
            self.__main_procedure()
        except KeyboardInterrupt:
            print('KeyboardInterrupt, exiting...')
            self.exiting = True
        except Exception as e:
            print('Error in main procedure, exiting...')
            print(e)
            self.exiting = True

        self.server_connection_thread.join()
        self.gi_dialog_auto_click_thread.join()

    def __server_connection_procedure(self):
        print('server connection thread started')
        while not self.exiting:
            if self.remote_on and self.socket is None:
                try:
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket.connect((self.server_ip, self.server_port))
                    print('connected to server', self.server_ip, ':', self.server_port)
                except Exception as e:
                    self.socket = None
            time.sleep(1)
        if self.socket is not None:
            self.socket.close()

    def __gi_dialog_auto_click_procedure(self):
        print('genshin dialog auto click thread started')
        while not self.exiting:
            try:
                time.sleep(0.2)
                if self.gi_dialog_auto_click:
                    self.__send_event((0, event_utils.VJOY_CROSS, 1))
                time.sleep(0.2)
                if self.gi_dialog_auto_click:
                    self.__send_event((0, event_utils.VJOY_CROSS, 0))
            except Exception as e:
                print(e)

    def __init_joystick(self):
        print('initializing joystick...')
        self.joystick = self.pygame.joystick.Joystick(0)
        self.joystick.init()

    def __send_event(self, vjoy_event):
        if self.remote_on and self.socket is not None:
            try:
                self.socket.send(event_utils.encode_vjoy_event(vjoy_event))
            except Exception as e:
                print('Remote connection lost...')
                print(e)
                self.socket = None

        if self.local_on:
            event_utils.run_vjoy_event(self.vjoy, event_utils.decode_vjoy_event(event_utils.encode_vjoy_event(vjoy_event)))

    def __init_keypress(self):
        self.l1_pressed = False
        self.r1_pressed = False

        self.triangle_pressed = False
        self.triangle_released = False
        
        self.cross_pressed = False
        self.cross_released = False
        
        self.circle_pressed = False
        self.circle_released = False

        self.square_pressed = False
        self.square_released = False

    def __record_keypress(self, vjoy_event):
        # l1
        if vjoy_event[1] == event_utils.VJOY_L1:
            self.l1_pressed = vjoy_event[2] == 1
    
        # r1
        if vjoy_event[1] == event_utils.VJOY_R1:
            self.r1_pressed = vjoy_event[2] == 1
        
        # triangle
        self.triangle_released = vjoy_event[1] == event_utils.VJOY_TRIANGLE and self.triangle_pressed and vjoy_event[2] == 0
        if vjoy_event[1] == event_utils.VJOY_TRIANGLE:
            self.triangle_pressed = vjoy_event[2] == 1
        # cross
        self.cross_released = vjoy_event[1] == event_utils.VJOY_CROSS and self.cross_pressed and vjoy_event[2] == 0
        if vjoy_event[1] == event_utils.VJOY_CROSS:
            self.cross_released = self.cross_pressed and vjoy_event[2] == 0
            self.cross_pressed = vjoy_event[2] == 1
        # circle
        self.circle_released = vjoy_event[1] == event_utils.VJOY_CIRCLE and self.circle_pressed and vjoy_event[2] == 0
        if vjoy_event[1] == event_utils.VJOY_CIRCLE:
            self.circle_pressed = vjoy_event[2] == 1
        # square
        self.square_released = vjoy_event[1] == event_utils.VJOY_SQUARE and self.square_pressed and vjoy_event[2] == 0
        if vjoy_event[1] == event_utils.VJOY_SQUARE:
            self.square_pressed = vjoy_event[2] == 1

    def __process_macro(self):
        if not self.l1_pressed or not self.r1_pressed:
            return False
        if self.cross_released:
            self.gi_dialog_auto_click = not self.gi_dialog_auto_click
            if self.gi_dialog_auto_click:
                print('genshin dialog auto click enabled')
            else:
                print('genshin dialog auto click disabled')
        if self.triangle_released:
            self.local_on = True
            self.remote_on = True
            print('sync mode enabled')
        if self.circle_released:
            self.local_on = False
            self.remote_on = True
            print('remote only mode enabled')
        if self.square_released:
            self.local_on = True
            self.remote_on = False
            print('local only mode enabled')

    def __main_procedure(self):
        while not self.exiting:
            for event in pygame.event.get():
                vjoy_event = event_utils.event_pygame2vjoy(event)
                if vjoy_event is not None:
                    self.__record_keypress(vjoy_event)
                    if not self.__process_macro():
                        # only send event if not executing macro
                        self.__send_event(vjoy_event)
                else:
                    if event_utils.is_device_added(event):
                        self.__init_joystick()


class DupjoyServer:
    """
    Dupjoy Server will receive controller events and send them to vjoy
    """
    def __init__(self, port):
        self.port = port

    def start(self):
        self.exiting = False
        self.vjoy = pyvjoy.VJoyDevice(1)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(1)
        self.socket.settimeout(0.5)
    
        print('server started 0.0.0.0:{}'.format(self.port))
        self.__main_loop()
    
    def __main_loop(self):
        while not self.exiting:
            self.__accept_connection()

    def __accept_connection(self):
        try:
            try:
                self.socket.settimeout(0.5)
                conn, addr = self.socket.accept()
                print('connected to', addr)
                self.sock.settimeout(0.5)
                self.__read_data(conn)
            except socket.timeout:
                pass
            except Exception as e:
                print('connection interrupted...')
                print(e)
        except KeyboardInterrupt:
            print('KeyboardInterrupt, exiting...')
            self.exiting = True

    def __read_data(self, conn):
        while True:
            data = conn.recv(4)
            if data:
                event_utils.run_vjoy_event(self.vjoy, event_utils.decode_vjoy_event(data))
            else:
                print('connection closed...')
                break