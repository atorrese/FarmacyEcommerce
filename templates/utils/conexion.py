from utils.api_routeros import Api
from devices.models import DeviceInformation, InterfazInformation, IpInformation


class Info:
    user = 'tecnico'
    password = '0p3nmikrotik'
    port = 8729
    device = DeviceInformation()
    interfaz = InterfazInformation()
    address = IpInformation()

    # SENTENCES FOR INFORMATION OF FIRMWARE & DEVICE
    def get_status(self, target):
        connect = Api(target, user=self.user, password=self.password, port=self.port)
        request = connect.talk('/system/resource/print')
        request1 = connect.talk('/system/routerboard/print')
        data = request[0]
        data['Serie'] = request1[0].get('serial-number')
        self.device.model = data.get('board-name')
        self.device.os_version = data.get('version')
        self.device.architecture = data.get('architecture-name')
        self.device.uptime = data.get('uptime')
        self.device.cpu = data.get('cpu')
        self.device.cpu_frequency = data.get('cpu-frequency')
        self.device.serie = data.get('Serie')
        return self.device

    # SYSTEM IDENTITY

    # SENTENCE FOR GET SYSTEM IDENTITY
    def get_name(self, target, user, password, port):
        connect = Api(target, user=user, password=password, port=port)
        request = connect.talk('/system/identity/print')
        data = request[0]
        return data

    # SENTENCE FOR SET SYSTEM IDENTITY
    def set_name(self, target, user, password, port, name):
        connect = Api(target, user=user, password=password, port=port)
        command = ('/system/identity/set\n=name=' + name)
        request = connect.talk(command)
        return request

    # SENTENCE FOR GET INFORMATION OF INTERFACES
    def get_interface(self, target):
        connect = Api(target, user=self.user, password=self.password, port=self.port)
        request = connect.talk('/interface/print')
        data = []
        for interface in request:
            self.interfaz = InterfazInformation()
            self.interfaz.name = interface.get('name')
            self.interfaz.type = interface.get('type')
            self.interfaz.mtu = interface.get('mtu')
            self.interfaz.mac = interface.get('mac-address')
            self.interfaz.ldown = interface.get('link-downs')
            self.interfaz.lup = interface.get('last-link-up-time')
            data.append(self.interfaz)
        return data

    # INTERFACE VLAN

    # SENTENCE FOR GET INFORMATION OF INTERFACES VLAN
    def get_vlan(self, target, user, password, port):
        connect = Api(target, user=user, password=password, port=port)
        request = connect.talk('/interface/vlan/print')
        for interface in request:
            print('Name= ', interface.get('name'), '\n', 'Interface= ', interface.get('interface'), '\n',
                  'VLAN-ID= ', interface.get('vlan-id'), '\n', 'MTU= ', interface.get('mtu'), '\n',
                  'Running= ', interface.get('running'), '\n', 'Disable= ', interface.get('disable'))
        data = request[0]
        return data

    # SENTENCE FOR CREATE INTERFACE VLAN
    def add_vlan(self, target, user, password, port, name, vid, interface):
        connect = Api(target, user=user, password=password, port=port)
        command = ('/interface/vlan/add\n=name=' + name + '\n=vlan-id=' + vid + '\n=interface=' + interface)
        request = connect.talk(command)
        return request

    # SENTENCE FOR MODIFY INTERFACE VLAN
    def set_vlan(self, target, user, password, port, name, vid, interface, number):
        connect = Api(target, user=user, password=password, port=port)
        command = ('/interface/vlan/set\n=name=' + name + '\n=vlan-id=' + vid + '\n=interface=' + interface +
                   '\n=numbers=' + number)
        request = connect.talk(command)
        return request

    # SENTENCE FOR DELETE INTERFACE VLAN
    def delete_vlan(self, target, user, password, port, num):
        connect = Api(target, user=user, password=password, port=port)
        command = ('/interface/vlan/remove\n=numbers=' + num)
        request = connect.talk(command)
        return request

    # IP ADDRESS

    # SENTENCE FOR GET IP ADDRESS
    def get_ip_address(self, target):
        connect = Api(target, user=self.user, password=self.password, port=self.port)
        request = connect.talk('/ip/address/print')
        data = []
        for interface in request:
            self.address = IpInformation()
            self.address.number = interface.get('.id')
            self.address.address = interface.get('address')
            self.address.network = interface.get('network')
            self.address.interfaz = interface.get('actual-interface')
            self.address.dhcp = interface.get('dynamic')
            self.address.state = interface.get('disable')
            data.append(self.address)
        return data

    # SENTENCES FOR ADD IP ADDRESS
    def add_ip_address(self, target, address, interface, coment):
        connect = Api(target, user=self.user, password=self.password, port=self.port)
        command = ('/ip/address/add\n=address=' + address + '\n=interface=' + interface + '\n=comment=' + coment)
        request = connect.talk(command)
        return request

    # SENTENCE FOR MODIFY IP ADDRESS
    def set_ip_address(self, target, user, password, port, address, interface, coment, number):
        connect = Api(target, user=user, password=password, port=port)
        command = ('/ip/address/set\n=address=' + address + '\n=interface=' + interface + '\n=comment=' + coment +
                   '\n=numbers=' + number)
        request = connect.talk(command)
        return request

    # SENTENCE FOR DELETE IP ADDRESS
    def delete_ip_adress(self, target, user, password, port, num):
        connect = Api(target, user=user, password=password, port=port)
        command = ('/ip/address/remove\n=numbers=' + num)
        request = connect.talk(command)
        return request

    # IP FIREWALL FILTER

    # SENTENCES FOR GET IP FIREWALL FILTER
    def get_ip_firewall_filter(self, target, user, password, port):
        connect = Api(target, user=user, password=password, port=port)
        request = connect.talk('/ip/firewall/filter/print')
        for rule in request:
            print(rule)
            # for item in rule:
            # print(item, '= ', rule.get(item))
        data = request[0]
        return data

