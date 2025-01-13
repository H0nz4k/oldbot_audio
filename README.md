pro stažení na RPI5:
sudo apt update -y
sudo apt install git -y
git clone https://github.com/[vaše-uživatelské-jméno]/[název-repozitáře].git /opt/project
cd /opt/project
chmod +x install.sh
./install.sh
