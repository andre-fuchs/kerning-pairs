# UFOkerning 
More specific scripts for UFO kerning-related operations.  

---

### `convertFEAtoMMG.py`
Create a MetricsMachine Groups (MMG) file from a kern feature file.

__Dependencies:__ None
__Environment:__ command line  

```
python convertFEAtoMMG.py kern.fea
```

---

### `exportFLCfromUFO.py`
Dumps a FontLab Classes file (FLC) from a UFO.  
Assumes MetricsMachine-built class names.

__Dependencies:__ [defcon](https://github.com/typesupply/defcon)  
__Environment:__ command line  

```
python exportFLCfromUFO.py font.ufo
```

---

### `subsetUFOKerningAndGroups.py`
Subset kerning and groups in a UFO given a list of glyphs provided.  
Will export new plist files that can be swapped into the UFO.

__Dependencies:__ [defcon](https://github.com/typesupply/defcon)  
__Environment:__ command line  

```
python subsetUFOKerningAndGroups.py glyphList font.ufo
```
