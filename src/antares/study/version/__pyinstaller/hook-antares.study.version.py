from PyInstaller.utils.hooks import collect_data_files

hiddenimports = ['antares.study.version.create_app.resources']

datas = collect_data_files('antares.study.version.create_app.resources')