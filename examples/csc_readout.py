import pdb
import gatt


csc_measurement_service_uuid = "00001816-0000-1000-8000-00805f9b34fb"
csc_measurement_characteristic_uuid = "00002a5b-0000-1000-8000-00805f9b34fb"

class AnyDeviceManager(gatt.DeviceManager):
    def device_discovered(self, device):
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))

class AnyDevice(gatt.Device):
    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % self.mac_address)
    def connect_failed(self):
        super().connect_failed()
        print("[%s] Connection failed" % self.mac_address)
    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % self.mac_address)
    def services_resolved(self):
        super().services_resolved()
        print("[%s] resolved services" % self.mac_address)
        device_information_service = None
        cycle_information_service = None
        csc_characteristic = None
        #pdb.set_trace()
        for service in self.services:
            print("[%s] Service [%s]" % (self.mac_address, service.uuid))
            if service.uuid == '0000180a-0000-1000-8000-00805f9b34fb':
                device_information_service = service
                print(">> device_information_service uuid = %s" % device_information_service.uuid)
            elif service.uuid == csc_measurement_service_uuid:
                cycle_information_service = service
                print(">>>> cycle_information_service uuid = %s" % cycle_information_service.uuid)
            for characteristic in service.characteristics:
                if device_information_service is not None:
                    if service.uuid == device_information_service.uuid:
                        if characteristic.uuid == '00002a26-0000-1000-8000-00805f9b34fb':
                            firmware_version_characteristic = characteristic
                            print(">> firmware_version_characteristic  uuid = %s" % firmware_version_characteristic.uuid)
                            firmware_version_characteristic.read_value()
                if cycle_information_service is not None:
                    if service.uuid == csc_measurement_service_uuid:
                        if characteristic.uuid == csc_measurement_characteristic_uuid:
                            csc_characteristic = characteristic
                            print(">>>>>> csc_characteristic uuid = %s" % csc_characteristic.uuid)
                            csc_characteristic.enable_notifications()
                print("[%s]     Characteristic [%s]" % (self.mac_address, characteristic.uuid))
        firmware_version_characteristic.read_value()
    def characteristic_value_updated(self, characteristic, value):
        print("characteristic_value_updated callback for uuid %s" % characteristic.uuid)
        if characteristic.uuid == '00002a26-0000-1000-8000-00805f9b34fb':
            print("Firmware version: ", value.decode("utf-8"))
        elif characteristic.uuid == csc_measurement_characteristic_uuid:
            print("CSC update : %s" % value)

def service_demo(mac_address="DC:66:7D:AF:3A:08"):
    manager = gatt.DeviceManager(adapter_name = 'hci0')
    device = AnyDevice(mac_address, manager = manager)
    device.connect()
    manager.run()

def simple_demo():
    manager = AnyDeviceManager(adapter_name="hci0")
    manager.start_discovery()
    manager.run()


if __name__ == '__main__':
    #pdb.set_trace()
    service_demo()
#simple_demo()

