extends Node
var socket = WebSocketPeer.new()
var data = {}
var lastDataEntry = Time.get_ticks_msec()
var connectRetryTime = 2000 # msec
var connectingSince = Time.get_ticks_msec()
var status = ""

func GetData():
	return data

func Connect():
	print("Connecting to socket...")
	socket.connect_to_url("ws://localhost:37522")
	connectingSince = Time.get_ticks_msec()
	status = "Connecting"

func _ready() -> void:
	socket.inbound_buffer_size = 65535*10
	Connect()

func _process(delta):
	socket.poll()
	var state = socket.get_ready_state()
	
	if Time.get_ticks_msec() - connectingSince > connectRetryTime and state == 0:
		Connect()
	elif state == 0:
		status = "Retrying connection in " + str(2000 - (Time.get_ticks_msec() - connectingSince)) + "ms\nPlease enable the Sockets plugin!"

	
	if state == WebSocketPeer.STATE_OPEN:
		status = "Connected"
		var tempData = {}
		while socket.get_available_packet_count():
			var packet = socket.get_packet()
			# Decode it
			packet = packet.get_string_from_utf8()
			packet = packet.split(";")
			for packetData in packet:
				# Find the first :
				var index = 0
				for character in packetData:
					if character == ":":
						break
					index += 1

				if index == 0:
					continue
			
				if index == len(packetData):
					continue
					
				# Split the string
				var key = packetData.substr(0, index)
				var data = packetData.substr(index + 1, -1)
				
				# Convert to json if needed
				if "JSON" in key:
					key.replace("JSON", "")
					var json = JSON.new()
					var error = json.parse(data)
					if error == OK:
						data = json
					else:
						data = "Error parsing JSON: " + str(error_string(error))
					
				tempData.get_or_add(key)
				tempData[key] = data
		
		if tempData != {}:
			data = tempData
			lastDataEntry = Time.get_ticks_msec()
			# Acknowledge the packet
			socket.send_text("ok")
		
	elif state == WebSocketPeer.STATE_CLOSING:
		# Keep polling to achieve proper close.
		pass
		
	elif state == WebSocketPeer.STATE_CLOSED:
		var code = socket.get_close_code()
		var reason = socket.get_close_reason()
		print("WebSocket closed with code: %d, reason %s. Clean: %s" % [code, reason, code != -1])
		Connect()
