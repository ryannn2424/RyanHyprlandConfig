import argparse
import os

AUTOSETUP_VER = '1.0.0'

args = argparse.ArgumentParser(description='Automatic Config File Setup')
args.add_argument('-y', '--yes', action='store_true', help='Automatically answer yes to all prompts')
args.add_argument('-u', '--update', action='store_true', help='Update the script & config files')
args.add_argument('-v', '--version', action='version', version=AUTOSETUP_VER)

def HyprlandSetup(username, file_location_dir):
    print('\033[96mSymlinking Hyprland config files...\033[0m')
    try:
        if os.path.exists(f'/home/{username}/.config/hypr'):
            raise FileExistsError
        os.symlink(f'{file_location_dir}/hypr', f'/home/{username}/.config/hypr')

    except FileExistsError:
        print('\033[93mHyprland config files already exist. Skipping...\033[0m')

    except Exception as e:
        print(f'\033[91mError: {e}\033[0m')

def WaybarSetup(username, file_location_dir):
    print('\033[96mSymlinking Waybar config files...\033[0m')
    try:
        if os.path.exists(f'/home/{username}/.config/waybar'):
            raise FileExistsError
        os.symlink(f'{file_location_dir}/waybar', f'/home/{username}/.config/waybar')

    except FileExistsError:
        print('\033[93mWaybar config files already exist. Skipping...\033[0m')

    except Exception as e:
        print(f'\033[91mError: {e}\033[0m')

def WallpaperSetup(username, file_location_dir):
    print('\033[96mCopying Wallpaper config files...\033[0m')
    try:
        if not (os.path.exists(f'/home/{username}/Wallpapers')):
            os.mkdir(f'/home/{username}/Wallpapers')

        for file in os.listdir(f'{file_location_dir}/Wallpapers'):
            os.system(f'cp {file_location_dir}/Wallpapers/{file} /home/{username}/Wallpapers')

    except Exception as e:
        print(f'\033[91mError: {e}\033[0m')

def main(autoyes: bool = False):
    AutoYes = autoyes
    username = os.getlogin()
    file_location_dir = os.path.abspath(__file__).replace('setup.py', '')
    
    # Hyprland Setup
    if not AutoYes:
        print('\nWould you like to symlink the Hyprland config files? (y/n)')
        if input().lower() == 'y':
            HyprlandSetup(username, file_location_dir)
        else:
            print('Skipping Hyprland config file setup...')
    else:
        HyprlandSetup(username, file_location_dir)

    # Waybar Setup
    if not AutoYes:
        print('\nWould you like to symlink the Waybar config files? (y/n)')
        if input().lower() == 'y':
            WaybarSetup(username, file_location_dir)
        else:
            print('Skipping Waybar config file setup...')
    else:
        WaybarSetup(username, file_location_dir)
        

    # Wallpaper Setup
    if not AutoYes:
        print('\nWould you like to copy the Wallpaper config files? (y/n)')
        if input().lower() == 'y':
            WallpaperSetup(username, file_location_dir)
        else:
            print('Skipping Wallpaper config file setup...')

    print('Setup complete!')
        

if __name__ == '__main__':
    args = args.parse_args()
    if args.update:
        os.system('git pull')
        print("\033[91mPlease relaunch the script\033[0m")
        exit(0)
    elif args.yes:
        main(autoyes=True)
    else:
        main(autoyes=False)
