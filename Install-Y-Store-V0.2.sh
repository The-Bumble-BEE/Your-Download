#!/bin/bash
echo "Do you want to install Y-Store"
sudo apt install chromium-browser -y #Is used for creating Webapps
echo "Installing Chromium"
echo "DONE!"
echo "Installing Python3 with TkInter"
sudo apt-get install python3-tk -y
echo "DONE!"
echo "Installing dependences"
pip install --upgrade pip
pip install --upgrade pip setuptools
echo "Installing customtkinter"
pip install customtkinter 
echo "requests" 
pip install requests 
echo "DONE!"
echo "Downloading Your-Store"
echo "Installing"
cd /
sudo mkdir "/home/$USER/BumbleBee"
echo "Installing."
cd /home/$USER/BumbleBee
echo "Installing.."
sudo wget -O Your-Store-main.zip "https://github.com/The-Bumble-BEE/Your-Store/archive/main.zip"
echo "Installing..."
sudo unzip Your-Store-main.zip 'Your-Store-main/Your-Store-V.0.2/*' -d /home/$USER/BumbleBee
echo "Installing..."
sudo chmod -R 777 BumbleBee
echo "Installing...."
sudo rm Your-Store-main.zip
echo "Installing...."
read -p "Installation finished! Press Enter to close this window"
