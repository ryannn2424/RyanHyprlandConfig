### Credits
- [**@Anik200**](https://github.com/Anik200/) https://github.com/Anik200/dotfiles/tree/main/.config/waybar
    Pretty good waybar config - my version is slightly edited.

### Required Programs
- waybar
- hyprland
- hyprpaper
- rofi-wayland

Heres a quick command to install dependencies on Arch:
```bash
sudo pacman -S python3 waybar hyprland hyprpaper rofi-wayland
```

### Installation
1. Install the required Programs
2. Clone this repository
3. Run the install script using Python 3 (Or manually copy files in the config folder)

### Setup File
I created a setup file that dramaticlly simplifies the setup process (for new linux installs)
- Make sure to install the required programs first
- Run the setup file using Python (`python3 setup.py`)
- Additional options can be found by running `python3 setup.py --help`
