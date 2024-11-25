import argparse
import shutil
import os

AUTOSETUP_VER = '1.1.0'

args = argparse.ArgumentParser(description='Automatic Config File Setup')
args.add_argument('-y', '--yes', action='store_true', help='Automatically answer yes to all prompts')
args.add_argument('-u', '--update', action='store_true', help='Update the script & config files')
args.add_argument('-v', '--version', action='version', version=AUTOSETUP_VER)
args.add_argument('--hyprland', action='store_true', help='Automatically Setup ONLY Hyprland config files')
args.add_argument('--waybar', action='store_true', help='Automatically Setup ONLY Waybar config files')
args.add_argument('--wallpaper', action='store_true', help='Automatically Setup ONLY Wallpaper config files')
args.add_argument('--rofi', action='store_true', help='Automatically Setup ONLY Rofi config files')

def HyprlandSetup(username, file_location_dir):
    print('\033[96mSymlinking Hyprland config files...\033[0m')
    try:
        if os.path.exists(f'/home/{username}/.config/hypr'):
            raise FileExistsError
        os.symlink(f'{file_location_dir}/hypr', f'/home/{username}/.config/hypr', target_is_directory=True)

    except FileExistsError:
        print('\033[93mHyprland config files already exist. Skipping...\033[0m')

    except Exception as e:
        print(f'\033[91mError: {e}\033[0m')

def WaybarSetup(username, file_location_dir):
    print('\033[96mSymlinking Waybar config files...\033[0m')
    try:
        if os.path.exists(f'/home/{username}/.config/waybar'):
            raise FileExistsError
        os.symlink(f'{file_location_dir}/waybar', f'/home/{username}/.config/waybar', target_is_directory=True)

    except FileExistsError:
        print('\033[93mWaybar config files already exist. Skipping...\033[0m')

    except Exception as e:
        print(f'\033[91mError: {e}\033[0m')

def WallpaperSetup(username, file_location_dir):
    print('\033[96mCopying Wallpapers...\033[0m')
    try:
        if not (os.path.exists(f'/home/{username}/Wallpapers')):
            os.mkdir(f'/home/{username}/Wallpapers')

        for file in os.listdir(f'{file_location_dir}/Wallpapers'):
            os.system(f'cp {file_location_dir}/Wallpapers/{file} /home/{username}/Wallpapers')

    except Exception as e:
        print(f'\033[91mError: {e}\033[0m')

def RofiSetup(username, file_location_dir):
    def LinkSetupFile(file_location_dir):
        try:
            if os.path.exists(f'{file_location_dir}/configs/rofi/'):
                raise FileExistsError

            else:
                os.symlink(f'{file_location_dir}/configs/rofi/', f'/home/{username}/.config/rofi', target_is_directory=True)

        except FileExistsError:
            print('\033[93mRofi config files already exist. Skipping...\033[0m')

        except Exception as e:
            print(f'\033[91mError: {e}\033[0m')


    print('\033[96mFetching rofi theme files...\033[0m')
    try:
        file_link = 'https://raw.githubusercontent.com/newmanls/rofi-themes-collection/refs/heads/master/themes/spotlight-dark.rasi'
        config_dir = f'/home/{username}/.local/share/rofi/themes'

        if not os.path.exists(config_dir):
            os.mkdir(config_dir)

        if os.path.exists(f'{config_dir}/spotlight.rasi'):
            raise FileExistsError

        if shutil.which('wget'):
            # Download with wget if installed
            os.system(f'wget {file_link} -O {config_dir}/spotlight.rasi')
            
        elif shutil.which('curl'):
            # Download with curl if installed
            os.system(f'curl {file_link} -o {config_dir}/spotlight.rasi')

        else:
            raise shutil.ExecError

        LinkSetupFile(file_location_dir)

    except shutil.ExecError:
        print('\033[91mError: wget or curl not found. Cannot download rofi config files.\033[0m')

    except FileExistsError:
        print('\033[93mRofi config files already exist. Copying setup file...\033[0m')
        LinkSetupFile(file_location_dir)

def main(autoyes: bool = False):
    AutoYes = autoyes
    username = os.getlogin()
    file_location_dir = os.path.abspath(__file__).replace('setup.py', '')

    setups = {
        'Hyprland': [
            '\nWould you like to symlink the Hyprland config files? (y/n)',
            HyprlandSetup,
            'Skipping Hyprland config file setup...'
        ],
        'Waybar': [
            '\nWould you like to symlink the Waybar config files? (y/n)',
            WaybarSetup,
            'Skipping Waybar config file setup...'
        ],
        'Wallpaper': [
            '\nWould you like to copy the Wallpapers (y/n)',
            WallpaperSetup,
            'Skipping Wallpaper config file setup...'
        ],
        'Rofi': [
            '\nWould you like to setup the Rofi config files? (y/n)',
            RofiSetup,
            'Skipping Rofi config file setup...'
        ]
    }
    
    # Did this to condense the code a little bit
    for setup_option in setups:
        if not AutoYes:
            print(setups[setup_option][0])
            if input().lower() == 'y':
                setups[setup_option][1](username, file_location_dir)
            else:
                print(setups[setup_option][2])
        else:
            setups[setup_option][1](username, file_location_dir)
   
    print('Setup complete!')
        

if __name__ == '__main__':
    args = args.parse_args()
    if args.update:
        os.system('git pull')
        print("\033[91mPlease relaunch the script\033[0m")
        exit(0)
    elif args.hyprland:
        HyprlandSetup(os.getlogin(), os.path.abspath(__file__).replace('setup.py', ''))
    elif args.waybar:
        WaybarSetup(os.getlogin(), os.path.abspath(__file__).replace('setup.py', ''))
    elif args.wallpaper:
        WallpaperSetup(os.getlogin(), os.path.abspath(__file__).replace('setup.py', ''))
    elif args.rofi:
        RofiSetup(os.getlogin(), os.path.abspath(__file__).replace('setup.py', ''))
    elif args.yes:
        main(autoyes=True)
    else:
        main(autoyes=False)
