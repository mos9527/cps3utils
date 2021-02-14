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

### 中文使用说明
本脚本适用于对 FBA (combined) rom 与 FBNeo、游聚 (split) rom 的转换

##### FBA -> FBN (combined -> split)
  即把 10、20形式 rom 转为 `jojoba-simm1.0` 形式 rom

    python rom_conversion.py split [FBA rom解压后文件夹] [FBN rom输出文件夹]

##### FBN -> FBA (split -> combined)
  即把  `jojoba-simm1.0` 形式 rom 转为 10、20形式 rom

    python rom_conversion.py combine [FBN rom解压后文件夹] [FBA rom输出文件夹]
  
注：输出文件夹不含 u2 (bios) 文件，请务必手动添加后打包