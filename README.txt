    ____       _       __               ______                         ________              __  
   / __ \_____(_)___  / /____  _____   /_  __/___  ____  ___  _____   / ____/ /_  ___  _____/ /__
  / /_/ / ___/ / __ \/ __/ _ \/ ___/    / / / __ \/ __ \/ _ \/ ___/  / /   / __ \/ _ \/ ___/ //_/
 / ____/ /  / / / / / /_/  __/ /       / / / /_/ / / / /  __/ /     / /___/ / / /  __/ /__/ ,<   
/_/   /_/  /_/_/ /_/\__/\___/_/       /_/  \____/_/ /_/\___/_/      \____/_/ /_/\___/\___/_/|_|  
                                                                                                 

The purpose of this program is to periodically check the toner levels on network printers.

The script will only work for Ricoh and HP printers.

To run SNMP walk on Windows 64 bit, install the program from the following link:
https://sourceforge.net/projects/net-snmp/files/net-snmp%20binaries/5.5-binaries/


------------------------------------------------ How To Use This Program -------------------------------------------------

- Update the 'printerIP' file with the desired printers or make your own file; make sure to maintain the same format.

- Comment out the 'ssh()' function call if not accessing printers on a different network.

- Set Windows Task Scheduler to run the 'printer' bat file at any given interval.


For accessing printers on a different network

- Update the 'yardPrinterIP' file if accessing network printers on a different network.

- A computer that is accessible from the outside needs to be always on at the remote location.

- Update the 'ssh()' function with the proper credentials to access the remote computer

- Both 'yardPrinterIP' and 'yardPrinters' should be stored locally on the computer at the default directory when SSH'ing.

