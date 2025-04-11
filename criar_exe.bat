@echo off
echo Gerando EXE com PyInstaller...

REM Remove a pasta dist antiga (se quiser manter, comente essa linha)
rmdir /s /q dist

REM Executa o PyInstaller com o .spec
pyinstaller jogo.spec

echo.
echo ✅ Finalizado! Verifique a pasta "dist\jogo".
pause
