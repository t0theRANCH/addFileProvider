Add File Provider for Python/Buildozer
=================

Tired of manually adding the file provider code to your Android 
Manifest template in your python for android app?
Automatically add a file provider to your Python/Kivy app 
compiled with Buildozer using this script.

Just edit the "PROJECT_DIRECTORY" variable to whatever directory you
put your projects in, run the script, and follow the prompt.
When it asks "Input directory path you wish to access with the file 
provider", this will be the directory in your app that you want to add to
your "file_paths.xml" file, without the "/app/".

The script will automagically check for the appropriate code 
(and add it if it isn't there) in your Android Manifest, 
and make a "file_paths.xml" for whichever app you select in the prompt. 