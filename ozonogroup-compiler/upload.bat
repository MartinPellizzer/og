robocopy .\public ..\ozonogroup\ /E
cd ..
cd ozonogroup
git add .
git commit -m "'"
git push
cd ..
cd ozonogroup-compiler