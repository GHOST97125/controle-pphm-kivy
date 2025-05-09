[app]
title = Controle PPHM
package.name = controlepphm
package.domain = org.pphmcontrole
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,plyer,reportlab
orientation = portrait
fullscreen = 1
osx.python_version = 3
osx.kivy_version = 2.3.0
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/splash.png
android.permissions = CAMERA,INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = armeabi-v7a, arm64-v8a
android.requirements = python3,kivy,plyer,reportlab
android.entrypoint = org.kivy.android.PythonActivity
android.allow_backup = True
android.logcat_filters = *:S python:D
android.useandroidnativeactivity = False
android.new_browser_state = 1

[buildozer]
log_level = 2
warn_on_root = 1
