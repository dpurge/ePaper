%echo off
set myfont=tahoma.ttf

pushd %~dp0

for %%S in (32 48 64) do (
    rem python font_to_py.py %myfont% %%S font_vie_%%S.py -k vietnamese
    python font_to_py.py %myfont% %%S font_pol_%%S.py -k polish --xmap
)

popd