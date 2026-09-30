#!/usr/bin/env python3

import os

VARIATIONS = ["20.3-Mint-Y-Luka",
              "20.3-Mint-Y-Luka-Dark"]

DEST = '../../usr/share/themes'

curdir = os.getcwd()

def updateLibadwaita(version:str) -> None:
    print(f"Updating LibAdwaita-{version} assets")
    os.chdir(f"libadwaita-{version}/")
    os.system("pysassc ./sass/gtk.scss defaults-light.css")
    os.system("pysassc ./sass/gtk-dark.scss defaults-dark.css")
    os.system("./render-assets.sh")
    print(f"LibAdwaita-{version} assets updated")

updateLibadwaita("1.5")
os.chdir(curdir)
updateLibadwaita("1.7")
os.chdir(curdir)
updateLibadwaita("1.9")
os.chdir(curdir)

print("Updating Gtk4 assets")
os.chdir("gtk-4.0/")
os.system("pysassc ./sass/gtk.scss gtk.css")
os.system("pysassc ./sass/gtk-dark.scss gtk-dark.css")
os.system("./render-assets.sh")
print("Gtk4 assets updated")

os.chdir(curdir)

print("Updating Gtk3 assets")
os.chdir("gtk-3.0/")
os.system("pysassc ./sass/gtk.scss gtk.css")
os.system("pysassc ./sass/gtk-dark.scss gtk-dark.css")
os.system("./render-assets.sh")
print("Gtk3 assets updated")

os.chdir(curdir)

print("Updating Gtk2 assets")
os.chdir("gtk-2.0/")
os.system("./render-assets.sh")
os.system("./render-dark-assets.sh")
print("Gtk2 assets updated")

os.chdir(curdir)

print("Updating Cinnamon assets")
os.chdir("cinnamon/")
os.system("pysassc ./sass/cinnamon.scss cinnamon.css")
os.system("pysassc ./sass/cinnamon-dark.scss cinnamon-dark.css")
print("Cinnamon assets updated")

os.chdir(curdir)

print("Updating Xfwm4 assets")
os.chdir("xfwm4/")
os.system("./render-assets.sh")

os.chdir(curdir)

print("Updating Xfwm4 dark assets")
os.chdir("xfwm4-dark/")
os.system("./render-assets.sh")

os.chdir(curdir)

def buildLibadwaita(version:str) -> None:
    version_folder = os.path.join(dest_folder, f"libadwaita-{version}")
    os.system(f"mkdir -p {version_folder}")
    os.system(f"cp -R libadwaita-{version}/assets %s" % version_folder)
    os.system(f"cp libadwaita-{version}/defaults-light.css %s/base.css" % version_folder)
    os.system(f"touch {version_folder}/defaults-light.css {version_folder}/defaults-dark.css")

def somethingLibadwaita(version:str) -> None:
    version_folder = os.path.join(dest_folder, f"libadwaita-{version}")
    os.system("mkdir -p %s" % version_folder)
    os.system(f"cp -R libadwaita-{version}/assets %s" % version_folder)
    os.system(f"cp libadwaita-{version}/defaults-dark.css %s" % os.path.join(version_folder, "base.css"))
    os.system(f"touch {version_folder}/defaults-light.css {version_folder}/defaults-dark.css")

if __name__ == '__main__':
    print("Building themes")
    for variation in VARIATIONS:
        dest_folder = os.path.join(DEST, variation)
        os.system("mkdir -p %s" % dest_folder)
        if variation == "20.3-Mint-Y-Luka":
            print("    Building 20.3-Mint-Y-Luka")
            os.system("cp index.theme %s/" % dest_folder)
            # Gtk2
            version_folder = os.path.join(dest_folder, "gtk-2.0")
            os.system("mkdir -p %s" % version_folder)
            os.system("cp -R gtk-2.0/assets %s" % version_folder)
            os.system("cp gtk-2.0/*.rc %s" % version_folder)
            os.system("cp gtk-2.0/gtkrc %s" % version_folder)
            # Gtk3
            version_folder = os.path.join(dest_folder, "gtk-3.0")
            os.system("mkdir -p %s" % version_folder)
            os.system("cp -R gtk-3.0/assets %s" % version_folder)
            os.system("cp gtk-3.0/gtk.css %s" % version_folder)
            os.system("cp gtk-3.0/gtk-dark.css %s" % version_folder)
            os.system("cp gtk-3.0/thumbnail.png %s" % version_folder)
            # Gtk4
            version_folder = os.path.join(dest_folder, "gtk-4.0")
            os.system("mkdir -p %s" % version_folder)
            os.system("cp -R gtk-4.0/assets %s" % version_folder)
            os.system("cp gtk-4.0/gtk.css %s" % version_folder)
            os.system("cp gtk-4.0/gtk-dark.css %s" % version_folder)
            # LibAdwaita
            buildLibadwaita("1.5")
            buildLibadwaita("1.7")
            buildLibadwaita("1.9")
            # Metacity
            os.system("cp -R metacity-1 %s" % dest_folder)
            # Cinnamon
            version_folder = os.path.join(dest_folder, "cinnamon")
            os.system("mkdir -p %s" % version_folder)
            os.system("cp -R cinnamon/common-assets %s" % version_folder)
            os.system("cp -R cinnamon/light-assets %s" % version_folder)
            os.system("cp cinnamon/20.3-mint-Y-Luka-thumbnail.png %s" % os.path.join(version_folder, "thumbnail.png"))
            os.system("cp cinnamon/cinnamon.css %s" % version_folder)
            # XFWM
            version_folder = os.path.join(dest_folder, "xfwm4")
            os.system("mkdir -p %s" % version_folder)
            os.system("cp -R xfwm4/*.png %s" % version_folder)
            os.system("cp -R xfwm4/themerc %s" % version_folder)
            # Openbox
            version_folder = os.path.join(dest_folder, "openbox-3")
            os.system ("mkdir -p %s" % version_folder)
            os.system("cp openbox-3/themerc %s/themerc" % (version_folder))
        elif variation == "20.3-Mint-Y-Luka-Dark":
            print("    Building 20.3-Mint-Y-Luka-Dark")
            os.system("cp index.theme-dark %s" % os.path.join(dest_folder, "index.theme"))
            # Gtk2
            version_folder = os.path.join(dest_folder, "gtk-2.0")
            os.system("mkdir -p %s" % version_folder)
            os.system("cp -R gtk-2.0/assets-dark %s" % version_folder)
            os.system("rm -rf %s" % os.path.join(version_folder, "assets"))
            os.system("mv %s %s" % (os.path.join(version_folder, "assets-dark"), os.path.join(version_folder, "assets")))
            os.system("cp gtk-2.0/*.rc %s" % version_folder)
            os.system("cp gtk-2.0/gtkrc-dark %s" % os.path.join(version_folder, "gtkrc"))
            os.system("cp gtk-2.0/menubar-toolbar-dark.rc %s" % os.path.join(version_folder, "menubar-toolbar.rc"))
            # Gtk3
            version_folder = os.path.join(dest_folder, "gtk-3.0")
            os.system("mkdir -p %s" % version_folder)
            os.system("cp -R gtk-3.0/assets %s" % version_folder)
            os.system("cp gtk-3.0/gtk-dark.css %s" % os.path.join(version_folder, "gtk.css"))
            os.system("cp gtk-3.0/gtk-dark.css %s" % os.path.join(version_folder, "gtk-dark.css"))
            os.system("cp gtk-3.0/thumbnail-dark.png %s" % os.path.join(version_folder, "thumbnail.png"))
            # Gtk4
            version_folder = os.path.join(dest_folder, "gtk-4.0")
            os.system("mkdir -p %s" % version_folder)
            os.system("cp -R gtk-4.0/assets %s" % version_folder)
            os.system("cp gtk-4.0/gtk-dark.css %s" % os.path.join(version_folder, "gtk.css"))
            os.system("cp gtk-4.0/gtk-dark.css %s" % os.path.join(version_folder, "gtk-dark.css"))
            # LibAdwaita
            somethingLibadwaita("1.5")
            somethingLibadwaita("1.7")
            somethingLibadwaita("1.9")
            # Cinnamon
            version_folder = os.path.join(dest_folder, "cinnamon")
            os.system("mkdir -p %s" % version_folder)
            os.system("cp -R cinnamon/common-assets %s" % version_folder)
            os.system("cp -R cinnamon/dark-assets %s" % version_folder)
            os.system("cp cinnamon/20.3-mint-Y-Luka-dark-thumbnail.png %s" % os.path.join(version_folder, "thumbnail.png"))
            os.system("cp cinnamon/cinnamon-dark.css %s" % os.path.join(version_folder, "cinnamon.css"))
            # XFWM
            version_folder = os.path.join(dest_folder, "xfwm4")
            os.system("mkdir -p %s" % version_folder)
            os.system("cp -R xfwm4-dark/*.png %s" % version_folder)
            os.system("cp -R xfwm4-dark/themerc %s" % version_folder)
            # Openbox
            version_folder = os.path.join(dest_folder, "openbox-3")
            os.system ("mkdir -p %s" % version_folder)
            os.system("cp openbox-3/themerc-dark %s/themerc" % (version_folder))
