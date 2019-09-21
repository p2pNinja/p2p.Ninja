echo "Thank you for choosing p2p.Ninja!!"
rm pathtohere
echo $(pwd)
(pwd)>>pathtohere
#crontab -l>logofcrontab
cd initialsetup/
sleep 5
lxterminal\
	--title="p2p.Ninja"\
	-e sudo python3 initialsetup.py
sleep 5