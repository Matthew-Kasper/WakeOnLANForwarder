# WakeOnLANForwarder
 Runs an http webserver on a Raspberry Pi Pico W to allow Wake On LAN capabilities over the internet.
 
 ### Environment Details
 * Must include a credentials.txt file in the root directory that includes the wifi ssid, wifi password, ip of device to be woken/killed, broadcast ip, device MAC address (All Capitals Bytes Only), and password to authenticate wake/kill operations. All of these fields should be on their own lines in order.
 * Must include a logs directory in the root directory for exception logging
 * Python files, credentials.txt, and the uping package must be flashed to a Raspberry Pi Pico W and ran with Micropython
