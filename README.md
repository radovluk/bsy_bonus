# bsy_bonus

I used pyUnicodeSteganography to encode messages

## Usage:

bot sends heartbeats and checks for command every 10 second
controller has following functions:

	- w (list of users currently logged in)
	- ls <PATH> (list content of specified directory)
	- id (if of current user)
	- Copy a file from the bot to the controller. The file name is specified
	- Execute a binary inside the bot given the name of the binary. Example: ‘/usr/bin/ps’

controller.send_command(self, command, path=None, file_name=None, binary_name=None)