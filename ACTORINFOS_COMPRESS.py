import shutil
import zipfile
import os

source_folder = 'Prefab_Characters/Prefab_Hero'
destination_folder = 'Prefab_Characters'

for subfolder in os.listdir(source_folder):
    subfolder_name = os.path.basename(subfolder)
    hero_id = subfolder_name.split('_')[0]
    zip_file_name = f"Actor_{hero_id}_Infos.pkg.bytes"
    zip_file = zipfile.ZipFile(os.path.join(destination_folder, zip_file_name), 'w')
    
    for file in os.listdir(os.path.join(source_folder, subfolder)):
        zip_file.write(os.path.join(source_folder, subfolder, file))
    
    zip_file.close()

parent_dir = 'Prefab_Characters'
for item in os.listdir(parent_dir):
    item_path = os.path.join(parent_dir, item)
    if os.path.isdir(item_path):
        shutil.rmtree(item_path)
    elif item in ['Prefab_Hero.zip', 'Prefab_Monster.pkg.bytes', 'Prefab_Organ.pkg.bytes', 'Prefab_Soldier.pkg.bytes']:
        os.remove(item_path)
