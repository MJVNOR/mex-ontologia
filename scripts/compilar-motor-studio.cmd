@echo off
call "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"
if errorlevel 1 exit /b %errorlevel%
set "LIBCLANG_PATH=C:\Program Files\LLVM\bin"
cd /d "C:\Users\marti\Documents\open-ontologies"
cargo build --locked --release --bin open-ontologies
exit /b %errorlevel%
