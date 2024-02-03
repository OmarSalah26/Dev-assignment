#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask

from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from apscheduler.schedulers.background import BackgroundScheduler

class SystemPerformanceManager(object):
	"""
	Shell representation of class for student implementation.
	
		"""
	def __init__(self):
		configUtil = ConfigUtil()
	
		self.pollRate = \
			configUtil.getInteger( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.POLL_CYCLES_KEY, defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
		
		self.locationID = \
			configUtil.getProperty( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		if self.pollRate <= 0:
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
			
		self.dataMsgListener = None
		
		# NOTE: The next four SLOC's are new for this task
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job(self.handleTelemetry, 'interval', seconds = self.pollRate)
		
		self.cpuUtilTask = SystemCpuUtilTask()
		self.memUtilTask = SystemMemUtilTask()

	def handleTelemetry(self):
		cpuUtilPct = self.cpuUtilTask.getTelemetryValue()
		memUtilPct = self.memUtilTask.getTelemetryValue()
		
		logging.debug('CPU utilization is %s percent, and memory utilization is %s percent.', str(cpuUtilPct), str(memUtilPct))
		
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		pass
	
	def startManager(self):
		logging.info("Starting SystemPerformanceManager...")
		
		if not self.scheduler.running:
			self.scheduler.start()
			logging.info("Started SystemPerformanceManager.")
		else:
			logging.warning("SystemPerformanceManager scheduler already started. Ignoring.")
			
		
	def stopManager(self):
		logging.info("Stopping SystemPerformanceManager...")
	
		try:
			self.scheduler.shutdown()
			logging.info("Stopped SystemPerformanceManager.")
		except:
			logging.warning("SystemPerformanceManager scheduler already stopped. Ignoring.")
