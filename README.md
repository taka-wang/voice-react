# voice-react

## Install

```
git clone to /home/pi/snips_butterfly/ folder
sudo pip install paho-mqtt==1.3.1
sudo cp snips-butterfly.service /etc/systemd/system/multi-user.target.wants/
sudo systemctl daemon-reload
sudo systemctl start snips-butterfly
sudo systemctl status snips-butterfly
```
