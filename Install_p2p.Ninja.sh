echo "Thank you for choosing p2p.Ninja!!"
echo $(pwd)
(pwd)>>pathtohere
#crontab -l>logofcrontab
#sleep (5)
lxterminal\
	--title="p2p.Ninja"\
	-e sudo python3 initialsetup.py
sleep 5