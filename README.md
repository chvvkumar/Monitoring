

# Monitor ESXi, Synology, Docker, PiHole, Plex and Raspberry Pi and Windows using Grafana, InfluxDB and Telegraf

## Demo

https://grafana.challa.co

## Screenshots:

Synology Dashboard
![Synology Dashboard](../Screenshots/synology.png)

Plex:
![Plex](../Screenshots/plex.png)

PiHole Dashboard
![PiHole Dashboard](../Screenshots/pihole.png)

ESXi Dashboard
![ESXi Dashboard](../Screenshots/esxi.png)

Windows
![Windows](../Screenshots/windows.png)

Raspberry Pi Dashboard
![Raspberry Pi Dashboard](../Screenshots/rpi.png)

Docker Dashboard
![Docker Dashboard](../Screenshots/docker.png)

Asuswrt-Merlin Router (ASUS RT-AC68):
![ASUS RT-AC68](../Screenshots/router_merlin.png)

## **Monitoring Raspberry Pi stats:**

Download "telegraf_pi_temp.sh" and 'chmod +x' the script. Then call it from within telegraf using "[[inputs.exec]]" (already included telegraf.conf in this repo).

## **Monitoring PiHole:**
Change the address of PiHole to your PiHole's address in telegraf.conf   


 4. Restart telegraf

## **Synology SNMP:**

Based on:
https://github.com/jperillo/Synology_dashboard_grafana

Make sure snmp-mibs-downloader is already installed on your telegraf host. It will download and install additional MIBs during install.

    apt-get install snmp-mibs-downloader
then

    download-mibs

1.  edit /etc/snmp/snmp.conf and comment out the 'mibs:' line. Here is what mine looks like:
    
    ```
      GNU nano 2.7.4                                                                                                                   
    File: /etc/snmp/snmp.conf
    # As the snmp packages come without MIB files due to license reasons, loading
    # of MIBs is disabled by default. If you added the MIBs you can reenable
    # loading them by commenting out the following line.
    # mibs :
    
    ```
    
2.  Now when you do a SNMPwalk, it will automatically translate OIDs to Names. This is what it looks like against my Synology:
    
    ```
    kumar@raspberrypi:~ $ snmpwalk -c public -v 2c 192.168.1.5
    SNMPv2-MIB::sysDescr.0 = STRING: Linux DiskStation 3.10.102 SMP Fri Jan 26 06:46:44 CST 2018 x86_64
    SNMPv2-MIB::sysObjectID.0 = OID: NET-SNMP-MIB::netSnmpAgentOIDs.10
    DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (90908998) 10 days, 12:31:29.98
    SNMPv2-MIB::sysContact.0 = STRING: Redacted
    SNMPv2-MIB::sysName.0 = STRING: Synology DS416Play
    SNMPv2-MIB::sysLocation.0 = STRING: Home
    
    ```
    
3.  Get your MIBs (from here, for Synology  [Synology MIB download](https://global.download.synology.com/download/Document/MIBGuide/Synology_MIB_File.zip)) and drop them in either of the below locations:


    
`/home/$USER/.snmp/mibs or user/share/snmp/mibs`

    
4.  Go through the linked page above or the snmpwalk output and make a list of OIDs you want to monitor (grep is your friend here)
    
5.  Add them to telegraf.conf using examples others have provided elsewhere in this thread
    
6.  Restart telegraf and test with the '-test' flag. To verify everything is working as expected.

## **VMWare Monitoring**

Telegraf introduced a new vsphere plugin. I will be using this instead of a custom script going forward. This plugin and details can be found here:

https://github.com/influxdata/telegraf/tree/master/plugins/inputs/vsphere

Dashboards for the metrics can be found here:

https://github.com/jorgedlcruz/vmware-grafana


## Monitoring Docker:

**
DockerHost: Synology NAS (DS416Play)
Telegraf: Raspberry Pi

Since I did not want to mess around with exposing docker.sock file to a remote client, I went with exposing a TCP endpoint on docker host to a remote telegraf agent. 

To do this: 
 
 

 **1. On Docker Host (Synology):**

Add the endpoint details to /var/packages/Docker/etc/dockerd.json like so:

    admin@DiskStation:~$ cat /var/packages/Docker/etc/dockerd.json
    {
    	"hosts" : [ "tcp://synology.lan:2375", "unix:///var/run/docker.sock" ],
    	"registry-mirrors" : []
    }

In the above snippet, `tcp://synology.lan:2375` Is the end point definition we have to add

*Note:* Don't change any part of the "unix:///var/run/docker.sock" definition. Synology uses to run the Docker GUI. Also, since this is a JSON file, all lines except the last line have a " , " at the end. Also note the " , " after the TCP definition.

If you want to be doubly sure, you can use https://jsonlint.com to validate the JSON contents.

Once this is done, restart the docker package from within DSM's Package center

 **2. On Telegraf:**
Add the below lines to your input plugins:

    # Synology Docker
    [[inputs.docker]]
      endpoint = "tcp://synology.lan:2375"
      container_names = []

 **3. Grafana Dashboard:**

Grafana Dashboard JSON is included in this repository. Simply import it, define your data source and you should be good to go.

## **Plex Monitoring**

Plex can be monitored using Verken linked below. I have included my customized dashboard in the repo for reference.

https://github.com/Boerderij/Varken
