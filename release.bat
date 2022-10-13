call .\venv\Scripts\activate.bat
fbs freeze
copy venv\Lib\site-packages\cv2\opencv_ffmpeg410_64.dll .\target\MyFbsApp
xcopy venv\Lib\site-packages\qt_material .\target\MyFbsApp /E
pause