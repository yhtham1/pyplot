@echo off
call d:\bin\usepy3.cmd
cd /d %~dp0
python pyplot_mrp.pyw color SN %1 %2 %3 %4 %5 %6 %7 %8 %9
