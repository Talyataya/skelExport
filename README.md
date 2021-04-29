# skelExport
skelExport is a Blender Addon for exporting skeleton into a format usable in Arma 3 model.cfg files.

## Features
* Export of the chosen object's armature in skeletonBones format for Arma 3.

## Installation

Blender:
* 'Edit' -> 'Preferences'
* Select the 'Add-ons' tab
* 'Install...'
* Navigate to the 'skelExport.py' file and select it
* Install it by pressing 'Install Add-on from File...'
* Enable the addon by setting the checkmark in front of it

## Known Issues
Please report any issues at https://github.com/talyataya/skelExport/issues

## Usage ##
Blender:
* Go to 'File' -> 'Export' -> 'Arma 3 Skeleton (.hpp)'
* Set the export options
    * 'Object': Object with Armature.
	* 'Retrieve Parents': If active, sets parents according to Armature hierarchy; otherwise bone is defined without parent.
    * 'Config Entry Mode': Converts output to skeletonBones={output}.
	
* Navigate the directory tree and set/select the file name (existing files will be OVERWRITTEN)
* 'Export skeletonBones'