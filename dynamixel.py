from dynamixel_sdk import *
import Adafruit_BBIO.GPIO as GPIO
import time  

# Control table address
ADDR_PRO_TORQUE_ENABLE      = 64               # Control table address is different in Dynamixel model
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132

# Data Byte Length
LEN_PRO_GOAL_POSITION       = 4
LEN_PRO_PRESENT_POSITION    = 4

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 100           # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 4000            # and this value (note that the Dynamixel would not move when the position value is out of movable range. 
											  # Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold


def usleep(x): 
	time.sleep(x/1000000.0)

#########################
### MyDynamixel Class ###
#########################

class MyDynamixel:
	def __init__(self,ID, name):    # Use 1, 2 as the ID for our two motors
		self.id = ID
		self.name = name
		self.goal_position = 0
		self.reached_goal = False

	def EnableTorque(self, packetHandler, portHandler):
		id = self.id
		name = self.name
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
		if dxl_comm_result != COMM_SUCCESS:
			print("%s: %s" % (name, packetHandler.getTxRxResult(dxl_comm_result)))
		elif dxl_error != 0:
			print("%s: %s" % (name, packetHandler.getRxPacketError(dxl_error)))
		else:
			print("%s has been successfully connected" % name)

	def DisableTorque(self, packetHandler, portHandler):
		id = self.id
		name = str(self.name)
		dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, id, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
		if dxl_comm_result != COMM_SUCCESS:
			print("%s: %s" % (name, packetHandler.getTxRxResult(dxl_comm_result)))
		elif dxl_error != 0:
			print("%s: %s" % (name, packetHandler.getRxPacketError(dxl_error)))
		else:
			print("%s has been successfully disconnected" % str(name))

	def rotateMotor(self, angle, packetHandler, portHandler):
		#max rotation value = 4096
		self.readPresentPosition(packetHandler, portHandler)
		command = int((angle*4096)/(360))
		self.goal_position = self.present_position + command
		self.writeGoalPosition(self.goal_position, packetHandler, portHandler)
		while 1:
			self.readPresentPosition(packetHandler, portHandler)
			if not abs(self.goal_position - self.present_position) > DXL_MOVING_STATUS_THRESHOLD:
				break
