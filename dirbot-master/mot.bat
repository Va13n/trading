@echo off
FOR %%i IN (0 1 24) DO (
   echo ***
   echo %%i
   echo ***
   python f:\trading\dirbot-master\spiderwrapper.py %*
   timeout 300 > NUL
) 
