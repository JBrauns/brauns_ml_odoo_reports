@echo off

set WK_INST=C:\\Tools\\wkhtmltox
set "WK_EXE=%WK_INST%\\bin\\wkhtmltopdf.exe"
set WK_ARGS=--dpi 96 --header-line --log-level info --disable-smart-shrinking --margin-top 32 --margin-left 0 --footer-line --margin-bottom 32

if not exist out mkdir out

%WK_EXE% %WK_ARGS% --header-html header.html --footer-html footer.html body.html out/doc.pdf

out\doc.pdf