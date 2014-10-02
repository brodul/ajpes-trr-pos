ajpes-trr-pos
=============

Uvoznik transakcijskih racunov poslovnih subjektov (prek poizvedbe na AJPES) v relacijske baze


Opis XML datotek
++++++++++++++++
[Opis XML datotek](http://www.ajpes.si/ostale_vsebine/za_razvijalce_programske_opreme#DvaEnaEna) na strani AJPES.

Namestitev
++++++++++

Namestitev je mogoca na linux operacijskem sistemu.

Za namestitev potrebujete installliran paket git, python virtualenv
(python-virtualen na Ubuntu/Debian) .

Kot navaden uporabnik v zeljeni mapi pozenite naslednje ukaze

```sh
git clone https://github.com/brodul/ajpes-trr-pos.git
cd ajpes-trr-pos
virtualenv .
source bin/activate
python setup.py develop
hash -r
ajpes-importer konfiguracija.ini
```


