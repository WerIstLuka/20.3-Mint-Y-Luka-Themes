#!/usr/bin/python3
import os
import threading

from constants import Y_HEX_ACCENT1, Y_HEX_ACCENT2, Y_HEX_ACCENT3, Y_HEX_ACCENT4
from constants import y_hex_colors1, y_hex_colors2, y_hex_colors3, y_hex_colors4

def change_value (key, value, file):
    if value is not None:
        command = "sed -i '/%(key)s=/c\%(key)s=%(value)s' %(file)s" % {'key':key, 'value':value, 'file':file}
    else:
        command = "sed -i '/%(key)s=/d' %(file)s" % {'key':key, 'file':file}
    os.system(command)

def y_colorize_directory (path, variation):
    for accent in Y_HEX_ACCENT1:
        os.system(f"find {path} -name '*.*' -type f -exec sed -i 's/{accent}/{y_hex_colors1[variation]}/gI' {{}}  \\;")
    for accent in Y_HEX_ACCENT2:
        os.system("find %s -name '*.*' -type f -exec sed -i 's/%s/%s/gI' {}  \\;" % (path, accent, y_hex_colors2[variation]))
    for accent in Y_HEX_ACCENT3:
        os.system("find %s -name '*.*' -type f -exec sed -i 's/%s/%s/gI' {}  \\;" % (path, accent, y_hex_colors3[variation]))
    for accent in Y_HEX_ACCENT4:
        os.system("find %s -name '*.*' -type f -exec sed -i 's/%s/%s/gI' {}  \\;" % (path, accent, y_hex_colors4[variation]))

if os.path.exists("usr"):
    os.system("rm -rf usr/")

start_dir = os.getcwd()

os.system("mkdir -p usr/share/themes")

# Mint-Y #################################################################

curdir = os.getcwd()

os.chdir("src/20.3-Mint-Y-Luka")
os.system("./build-themes.py")
os.chdir(curdir)

# 20.3-Mint-Y-Luka color variations
def yDerivateGtk(color:str, lightDark:str, theme:str, gtk:str) -> None:
    # gtk3 and 4 have the same generation process unlike in build-themes so we can use 1 function for both
    os.system(f"cp -R src/20.3-Mint-Y-Luka/{gtk}/sass {theme}/{gtk}")
    y_colorize_directory(f"{theme}/{gtk}/sass", color)
    os.system(f"""
        cd {theme}/{gtk}
        pysassc ./sass/gtk-dark.scss gtk-dark.css
        pysassc ./sass/gtk{lightDark}.scss gtk.css
    """)

def yDerivateLibadwaita(color:str, lightDark:str, theme:str, gtk:str) -> None:
    # libadwaita also uses the same build process but has different output file names
    yDerivateGtk(color, lightDark, theme, gtk)
    os.system(f"""
        cd {theme}/{gtk}
        cp gtk{lightDark}.css base.css
        rm gtk.css gtk-dark.css
    """)

def yCleanupGtkSass(theme:str) -> None:
    for gtk in ["gtk-3.0", "gtk-4.0", "libadwaita-1.5", "libadwaita-1.7", "libadwaita-1.9"]:
        os.system(f"""
            cd {theme}
            rm -rf {gtk}/sass {gtk}.sass-cache
        """)

def yDerivateCinnamon(color:str, lightDark:str, theme:str) -> None:
    os.system(f"cp -R src/20.3-Mint-Y-Luka/cinnamon/sass {theme}/cinnamon/")
    y_colorize_directory(f"{theme}/cinnamon/sass", color)
    if lightDark == "-dark":
        os.system(f"cd {theme}/cinnamon; cp sass/cinnamon-dark.scss sass/cinnamon.scss")
    os.system(f"""
        cd {theme}/cinnamon; pysassc ./sass/cinnamon.scss cinnamon.css
        rm -rf sass .sass-cache
""")

def yDerivateOpenbox(curdir:str, theme:str, color:str) -> None:
    os.chdir(curdir)
    # for accent in Y_HEX_ACCENT1: is redundant because the command used file, that just generated the last file
    # in files (e.g. theme/libadwaita-1.7/default-dark.css) again. The output is unchanged with the line removed
    for accent in Y_HEX_ACCENT2:
        os.system(f"sed -i s'/{accent}/{y_hex_colors2[color]}/gI' {os.path.join(theme, "openbox-3", "themerc")}")

def yAccentRecolorFile(theme:str, color:str) -> None:
    files = []
    files.append(os.path.join(theme, "gtk-2.0", "gtkrc"))
    files.append(os.path.join(theme, "gtk-2.0", "main.rc"))
    files.append(os.path.join(theme, "gtk-2.0", "panel.rc"))
    files.append(os.path.join(theme, "gtk-2.0", "apps.rc"))
    files.append(os.path.join(theme, "gtk-2.0", "menubar-toolbar.rc"))
    for file in files:
        if not os.path.exists(file):
            continue

        for accent in Y_HEX_ACCENT1:
            os.system(f"sed -i s'/{accent}/{y_hex_colors1[color]}/gI' {file}")
        for accent in Y_HEX_ACCENT2:
            os.system(f"sed -i s'/{accent}/{y_hex_colors2[color]}/gI' {file}")

def accentRecolorDirectory(theme:str, color:str) -> None:
    directories = []
    directories.append(os.path.join(theme, "cinnamon/common-assets"))
    directories.append(os.path.join(theme, "cinnamon/light-assets"))
    directories.append(os.path.join(theme, "cinnamon/dark-assets"))
    for directory in directories:
        if os.path.exists(directory):
            y_colorize_directory(directory, color)

def copyAssets(lightDark:str, theme:str, path:str) -> None:
    os.system(f"rm -rf {theme}/libadwaita-1.9/assets")
    os.system(f"rm -rf {theme}/libadwaita-1.7/assets")
    os.system(f"rm -rf {theme}/libadwaita-1.5/assets")
    os.system(f"rm -rf {theme}/gtk-4.0/assets")
    os.system(f"rm -rf {theme}/gtk-3.0/assets")
    os.system(f"rm -rf {theme}/gtk-2.0/assets")
    os.system(f"cp -R {path}/gtk-2.0/assets{lightDark} {theme}/gtk-2.0/assets")
    os.system(f"cp -R {path}/xfwm4{lightDark}/*.png {theme}/xfwm4/")
    os.system(f"cp -R {path}/gtk-3.0/assets {theme}/gtk-3.0/assets")
    os.system(f"cp -R {path}/gtk-4.0/assets {theme}/gtk-4.0/assets")
    os.system(f"cp -R {path}/libadwaita-1.5/assets {theme}/libadwaita-1.5/assets")
    os.system(f"cp -R {path}/libadwaita-1.7/assets {theme}/libadwaita-1.7/assets")
    os.system(f"cp -R {path}/libadwaita-1.9/assets {theme}/libadwaita-1.9/assets")

def yGenTheme(color:str):
    for variant in ["", "-Dark"]:
        original_name = f"20.3-Mint-Y-Luka{variant}"
        path = os.path.join(f"src/20.3-Mint-Y-Luka/variations/{color}")
        lightDark = variant.lower()
        if not os.path.isdir(path):
            exit()

        print(f"Derivating {original_name}-{color}")

        # Copy theme
        theme = f"usr/share/themes/{original_name}-{color}"
        theme_index = os.path.join(theme, "index.theme")
        os.system(f"cp -R usr/share/themes/{original_name} {theme}")

        # Theme name
        for key in ["Name", "GtkTheme"]:
            change_value(key, "%s-%s" % (original_name, color), theme_index)

        for key in ["IconTheme"]:
            change_value(key, "%s-%s" % (original_name, color), theme_index)

        yDerivateGtk(color, lightDark, theme, "gtk-3.0")
        yDerivateGtk(color, lightDark, theme, "gtk-4.0")
        # gtk4 has to build before libadwaita because _common.scss is symlinked between them
        # libadwaita is built in order because the version specific files are symlinked across the directories
        yDerivateLibadwaita(color, lightDark, theme, "libadwaita-1.5")
        yDerivateLibadwaita(color, lightDark, theme, "libadwaita-1.7")
        yDerivateLibadwaita(color, lightDark, theme, "libadwaita-1.9")

        # remove sass files after gtk4 and libadwaita have been derived so symlinks stay intact until its finished
        yCleanupGtkSass(theme)

        yDerivateCinnamon(color, lightDark, theme)

        # Accent color
        yAccentRecolorFile(theme, color)

        # Remove metacity-theme-3.xml (it doesn't need to be derived since it's using GTK colors,
        # and Cinnamon doesn't want to list it)
        os.system(f"rm -f {os.path.join(theme, 'metacity-1', 'metacity-theme-3.xml')}")

        accentRecolorDirectory(theme, color)

        # Assets
        copyAssets(lightDark,theme, path)

        # Openbox theme
        yDerivateOpenbox(curdir, theme, color)

threads = []
for color in y_hex_colors1.keys():
    t = threading.Thread(target=yGenTheme, args=(color,))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

# Files
os.system("cp -R files/* ./")
