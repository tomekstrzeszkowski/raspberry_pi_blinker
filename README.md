# Motivation

In recent years, there has been a significant rise in the usage of digital devices across all age brackets, whether for work or leisure. Various therapeutic and management approaches have been suggested to address this issue, encompassing optical, medical, and ergonomic interventions.

One common recommendation from clinicians is to take regular breaks to reduce digital eye strain. This advice often includes following the 20-20-20 rule, which suggests taking breaks to focus on an object at least 20 feet (6 meters) away for at least 20 seconds every 20 minutes.

This project serves as a reminder to perform these exercises by toggling your external device on and off, ideally accompanied by a light indicator.

# Installation

Install python dependencies from the readme.txt.
Append content from `.bashrc.tail.example` to `.bashrc`.
Optional: run python `install.py` script. It will create sql lite database
that will be used to persist current state (not used in current version)

```
python install.py
```
# Hardware 

## Electrical components
 - Raspberry Pi Zero
 - Single Channel 5V Relay Module Board or Solid State Relay (ssr)
 - Push Button
 - Resistor pack
 - Solderless breadboard
 - Jumper wires
 - Old Phone Charger as a power supply for raspberry
 - Electric Socket and Wires
 - Some plastic elements for the cover, I used plexy glass and hot glue
 - External lighting device, I used a LED tape
 - Light sensor dedicated for raspberry or andruino as an optional component

Circuit diagram:
Channel connections (GPIO, Board):

Button:
 - GPIO 23, Board 16
 - GND, Board 14

Relay:
 - GPIO 2, Board 2
 - 3V Power, Board 1
 - GND, Board 9

Light sensor:
 - GPIO 24, Board 22
 - 3V Power, Board 17
 - GND, Board 20

Version with relay and button:
![raspberry-pi-zero-5](https://github.com/tomekstrzeszkowski/raspberry_pi_blinker/assets/40120335/d6e8e9a6-460b-4b76-8fe5-7d1bba4f82ce)



# Demo



https://github.com/tomekstrzeszkowski/raspberry_pi_blinker/assets/40120335/3894c255-9412-4990-88f2-7700c9ee27eb



