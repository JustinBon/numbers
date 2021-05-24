@ECHO OFF
cd vids
youtube-dl https://www.youtube.com/playlist?list=PLTPQcjlcvvXFtR0R91Gh5j9Xi8cq0oN3Y --playlist-start %1
cd ..
cd subs
youtube-dl https://www.youtube.com/playlist?list=PLTPQcjlcvvXFtR0R91Gh5j9Xi8cq0oN3Y --playlist-start %1 --write-auto-sub --skip-download