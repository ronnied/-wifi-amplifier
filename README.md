# wifi-amplifier
Version 2.0 of my Network Amplifier.

Twisted Python server runs a JSON API to control the core functions of the amplifier.

Uses a PT2314 as the main audio processor, controlled via i2c.

A TEA5767 radio module (also i2c controlled) allows reception of local FM radio stations.

An nginx server is used to serve the frontend GUI via http. Javascript communicates with the JSON API via the GUI.
