import base64

open_icon = open("../assets/connected.png", "rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "connected = %s" % b64str
f = open("../icon1.py", "w+")
f.write(write_data)
f.close()
