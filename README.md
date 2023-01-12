# BSY bonus assignment task 5

## The task

1. Your task is to write the bot code and the controller code. The bot will be the infected computer, and the controller is what you use to control the bots.

2. Both parts should use gist.github.com to communicate.

3. The goal is to run some of your bots as 'infected' computers in the github channel, and you also connect to this channel with your controller to control them.

4. The communication between the bots and the controller should not be easily detected as 'bots' in the channel, therefore all communication should look like normal English markdown or text (text, images and emojis are accepted). You should use some steganography technique to hide your messages as English.

5. The controller should check if the bots are alive periodically

6. The controller should give orders to the bot and the bot should answer the output of the orders
The minimum orders are the following commands:
	- w (list of users currently logged in)
	- ls <PATH> (list content of specified directory)
	- id (if of current user)
	- Copy a file from the bot to the controller. The file name is specified
	- Execute a binary inside the bot given the name of the binary. Example: ‘/usr/bin/ps’

7. Publish the whole code in github and put the link as a flag for this stage.


## Installation
In order to run project you need to run both bot.py and controller.py
```bash
./python3 bot.py
./python3 controller.py
```

The bot sends heartbeats every seconds to controller in order to tell him he is alive. Both Bot and Controller are peridocially checking new messages in gist every 10 seconds with long pooling.

I used pyUnicodeSteganography to encode messages. https://github.com/bunnylab/pyUnicodeSteganography

## Usage:
In controller.py run following commands to activate bot.


```bash
#list currently logged users:
controller.send_command("w")

#list content of specified directory:
controller.send_command("ls", path=path)

#get id (if of current user)
controller.send_command("id")

#Copy a file from the bot to the controller
controller.send_command("cp", file_name=file)

#Execute binary
controller.send_command("bin", binary_name=name)
```
