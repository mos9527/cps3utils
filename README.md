# cps3hacking
Tools for modding CPS3 ROMs

## rom_conversion.py
For inter-converting split-roms & combined-roms
#### Credit
[GaryButternubs/CPS3-ROM-Conversion](https://github.com/GaryButternubs/CPS3-ROM-Conversion "GaryButternubs/CPS3-ROM-Conversion") for the java version
Discord JJBAHFTF #rom-hacking for references
#### Usage
    usage: rom_conversion.py [-h] OPERATION GAME IN OUT
    
    CPS3 ROM Converstion tool
    
    positional arguments:
      OPERATION   Operation : combine (split->combined) split (combined->split)
      GAME        Game name (e.g. Jojos (JPN) is jojoban)
      IN          Where to locate the extracted sources
      OUT         Where to save