#!/usr/bin/env python
import roslib; roslib.load_manifest('bluetooth_weather')
import rospy
import dynamic_reconfigure.server
from bluetooth_weather.cfg import bluetooth_weatherConfig as ConfigType



# protected region customHeaders on begin #

import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()


# protected region customHeaders end #

from std_msgs.msg import Float32
from std_msgs.msg import Float32
from std_msgs.msg import Float32


class bluetooth_weather_impl:
	out_temperature = Float32()
	out_humidity = Float32()
	out_pressure = Float32()

	def	__init__(self):



		# protected region initCode on begin #

		# Clear any cached data because both bluez and CoreBluetooth have issues with
		# caching data and it going stale.
		ble.clear_cached_data()

		# Get the first available BLE network adapter and make sure it's powered on.
		adapter = ble.get_default_adapter()
		adapter.power_on()
		print('Using adapter: {0}'.format(adapter.name))

		# Disconnect any currently connected UART devices.  Good for cleaning up and
		# starting from a fresh state.
		print('Disconnecting any connected UART devices...')
		UART.disconnect_devices()

		# Scan for UART devices.
		print('Searching for UART device...')
		try:
			adapter.start_scan()
			# Search for the first UART device found (will time out after 60 seconds
			# but you can specify an optional timeout_sec parameter to change it).
			device = UART.find_device()
			if device is None:
				raise RuntimeError('Failed to find UART device!')
		finally:
			# Make sure scanning is stopped before exiting.
			adapter.stop_scan()

		print('Connecting to device...')
		device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
				  # to change the timeout.

		# Once connected do everything else in a try/finally to make sure the device
		# is disconnected when done.
		try:
			# Wait for service discovery to complete for the UART service.  Will
			# time out after 60 seconds (specify timeout_sec parameter to override).
			print('Discovering services...')
			UART.discover(device)

			# Once service discovery is complete create an instance of the service
			# and start interacting with it.
			uart = UART(device)
			print('uart = UART(device)')

		finally:
        		# Make sure device is disconnected on exit.
        		device.disconnect()
			print('device.disconnect()')


		# protected region initCode end #
		pass

	def	configure(self):
		# protected region configureCode on begin #
		# protected region configureCode end #
		pass

	def	update(self):
		# protected region updateCode on begin #

		# Now wait up to one minute to receive data from the device.
		print('Waiting up to 60 seconds to receive data from the device...')
		received = uart.read(timeout_sec=60)

		while received is not None:
		    print('Received: {0}'.format(received))
		    received = uart.read(timeout_sec=60)

		if received is not None:
		    # Received data, print it out.
		    #print('Received: {0}'.format(received))
		else:
		    # Timeout waiting for data, None is returned.
		    print('Received no data!')


		out_temperature = 0.0
		out_humidity = 0.0
		out_pressure = 0.0

		# protected region updateCode end #
		pass




class bluetooth_weather:
	def __init__(self):
		self.impl = bluetooth_weather_impl()
		self_dynrecon_server = dynamic_reconfigure.server.Server(ConfigType, self.config_callback)
		self.temperature = rospy.Publisher('temperature', Float32, queue_size=1)
		self.humidity = rospy.Publisher('humidity', Float32, queue_size=1)
		self.pressure = rospy.Publisher('pressure', Float32, queue_size=1)


	def run(self):
		self.impl.update()
		self.temperature.publish(self.impl.out_temperature)
		self.humidity.publish(self.impl.out_humidity)
		self.pressure.publish(self.impl.out_pressure)

	def config_callback(self, config, level):
		return config

if __name__ == "__main__":
	try:
		rospy.init_node('bluetooth_weather')
		n = bluetooth_weather()
		n.impl.configure()
		while not rospy.is_shutdown():
			n.run()
			rospy.sleep(0.5)

	except rospy.ROSInterruptException:
		print "Exit"
