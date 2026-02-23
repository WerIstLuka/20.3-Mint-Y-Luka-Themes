#!/usr/bin/python3
import os

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
        os.system("find %s -name '*.*' -type f -exec sed -i 's/%s/%s/gI' {}  \\;" % (path, accent, y_hex_colors1[variation]))
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
for color in y_hex_colors1.keys():
    for variant in ["", "-Dark"]:
        original_name = "20.3-Mint-Y-Luka%s" % variant
        path = os.path.join("src/20.3-Mint-Y-Luka/variations/%s" % color)
        if os.path.isdir(path):
            print("Derivating %s-%s" % (original_name, color))

            # Copy theme
            theme = "usr/share/themes/%s-%s" % (original_name, color)
            theme_index = os.path.join(theme, "index.theme")
            os.system("cp -R usr/share/themes/%s %s" % (original_name, theme))

            # Theme name
            for key in ["Name", "GtkTheme"]:
                change_value(key, "%s-%s" % (original_name, color), theme_index)

            for key in ["IconTheme"]:
                change_value(key, "%s-%s" % (original_name, color), theme_index)

            # Regenerate libadwaita-1.5 sass
            os.system("cp -R src/20.3-Mint-Y-Luka/libadwaita-1.5/sass %s/libadwaita-1.5/" % theme)
            y_colorize_directory("%s/libadwaita-1.5/sass" % theme, color)
            os.chdir("%s/libadwaita-1.5" % theme)

            # os.system("touch defaults-light.css defaults-dark.css")
            if (variant == "-Dark"):
                os.system("sassc ./sass/gtk-dark.scss base.css")
            else:
                os.system("sassc ./sass/gtk.scss base.css")

            os.system("rm -rf sass .sass-cache")
            os.chdir(curdir)

            # Regenerate GTK4 sass
            os.system("cp -R src/20.3-Mint-Y-Luka/gtk-4.0/sass %s/gtk-4.0/" % theme)
            y_colorize_directory("%s/gtk-4.0/sass" % theme, color)
            os.chdir("%s/gtk-4.0" % theme)

            if (variant == "-Dark"):
                os.system("cp sass/gtk-dark.scss sass/gtk.scss")
                os.system("sassc ./sass/gtk.scss gtk.css")
                # Add a gtk-dark.css (this is needed by libhandy/libadwaita apps when prefer-dark is on)
                os.system("pysassc ./sass/gtk-dark.scss gtk-dark.css")
            else:
                os.system("sassc ./sass/gtk-dark.scss gtk-dark.css")
                os.system("sassc ./sass/gtk.scss gtk.css")

            os.system("rm -rf sass .sass-cache")
            os.chdir(curdir)

            # Regenerate GTK3 sass
            os.system("cp -R src/20.3-Mint-Y-Luka/gtk-3.0/sass %s/gtk-3.0/" % theme)
            y_colorize_directory("%s/gtk-3.0/sass" % theme, color)
            os.chdir("%s/gtk-3.0" % theme)
            # os.system("sed -i 's/no-tint/tint/gI' ./sass/gtk.scss")
            # os.system("sed -i 's/no-tint/tint/gI' ./sass/gtk-dark.scss")
            if (variant == "-Dark"):
                os.system("cp sass/gtk-dark.scss sass/gtk.scss")
                os.system("sassc ./sass/gtk.scss gtk.css")
                # Add a gtk-dark.css (this is needed by libhandy/libadwaita apps when prefer-dark is on)
                os.system("pysassc ./sass/gtk-dark.scss gtk-dark.css")
            else:
                os.system("sassc ./sass/gtk-dark.scss gtk-dark.css")
                os.system("sassc ./sass/gtk.scss gtk.css")

            os.system("rm -rf sass .sass-cache")
            os.chdir(curdir)

            # Regenerate Cinnamon sass
            os.system("cp -R src/20.3-Mint-Y-Luka/cinnamon/sass %s/cinnamon/" % theme)
            y_colorize_directory("%s/cinnamon/sass" % theme, color)
            os.chdir("%s/cinnamon" % theme)
            if (variant == "-Dark"):
                os.system("cp sass/cinnamon-dark.scss sass/cinnamon.scss")
            os.system("sassc ./sass/cinnamon.scss cinnamon.css")
            os.system("rm -rf sass .sass-cache")
            os.chdir(curdir)

            # Accent color
            files = []
            files.append(os.path.join(theme, "gtk-2.0", "gtkrc"))
            files.append(os.path.join(theme, "gtk-2.0", "main.rc"))
            files.append(os.path.join(theme, "gtk-2.0", "panel.rc"))
            files.append(os.path.join(theme, "gtk-2.0", "apps.rc"))
            files.append(os.path.join(theme, "gtk-2.0", "menubar-toolbar.rc"))
            files.append(os.path.join(theme, "libadwaita-1.7", "defaults-light.css"))
            files.append(os.path.join(theme, "libadwaita-1.7", "defaults-dark.css"))
            for file in files:
                if os.path.exists(file):
                    for accent in Y_HEX_ACCENT1:
                        os.system("sed -i s'/%(accent)s/%(color_accent)s/gI' %(file)s" % {'accent': accent, 'color_accent': y_hex_colors1[color], 'file': file})
                    for accent in Y_HEX_ACCENT2:
                        os.system("sed -i s'/%(accent)s/%(color_accent)s/gI' %(file)s" % {'accent': accent, 'color_accent': y_hex_colors2[color], 'file': file})
                    for accent in Y_HEX_ACCENT3:
                        os.system("sed -i s'/%(accent)s/%(color_accent)s/gI' %(file)s" % {'accent': accent, 'color_accent': y_hex_colors3[color], 'file': file})
                    for accent in Y_HEX_ACCENT4:
                        os.system("sed -i s'/%(accent)s/%(color_accent)s/gI' %(file)s" % {'accent': accent, 'color_accent': y_hex_colors4[color], 'file': file})

            # Remove metacity-theme-3.xml (it doesn't need to be derived since it's using GTK colors, and Cinnamon doesn't want to list it)
            os.system("rm -f %s" % os.path.join(theme, "metacity-1", "metacity-theme-3.xml"))

            directories = []
            directories.append(os.path.join(theme, "cinnamon/common-assets"))
            directories.append(os.path.join(theme, "cinnamon/light-assets"))
            directories.append(os.path.join(theme, "cinnamon/dark-assets"))
            for directory in directories:
                if os.path.exists(directory):
                    y_colorize_directory(directory, color)

            # Assets
            os.system("rm -rf %s/libadwaita-1.5/assets" % theme)
            os.system("rm -rf %s/gtk-4.0/assets" % theme)
            os.system("rm -rf %s/gtk-3.0/assets" % theme)
            os.system("rm -rf %s/gtk-2.0/assets" % theme)
            if variant == "-Dark":
                os.system("cp -R %s/gtk-2.0/assets-dark %s/gtk-2.0/assets" % (path, theme))
                os.system("cp -R %s/xfwm4-dark/*.png %s/xfwm4/" % (path, theme))
            else:
                os.system("cp -R %s/gtk-2.0/assets %s/gtk-2.0/assets" % (path, theme))
                os.system("cp -R %s/xfwm4/*.png %s/xfwm4/" % (path, theme))
            os.system("cp -R %s/gtk-3.0/assets %s/gtk-3.0/assets" % (path, theme))
            os.system("cp -R %s/gtk-4.0/assets %s/gtk-4.0/assets" % (path, theme))
            os.system("cp -R %s/libadwaita-1.5/assets %s/libadwaita-1.5/assets" % (path, theme))


# Files
os.system("cp -R files/* ./")
