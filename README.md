# WakeOnLANForwarder
 Runs an http webserver on a Raspberry Pi Pico W to allow Wake On LAN capabilities over the internet.
 
 ### Environment Details
 * Must include a credentials.txt file that includes the wifi ssid, wifi password, ip of device to be woken/killed, and password to authenticate wake/kill operations
 * Must run the kill-on-lan server located in the device-side directory on the repository
 * Python files, credentials.txt, and the uping package must be flashed to a Raspberry Pi Pico W and ran with Micropython
