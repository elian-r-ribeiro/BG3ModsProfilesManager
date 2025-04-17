import os;
import shutil;
import customtkinter as ctk;
import json;

userDir = os.environ["USERPROFILE"];
baseDir = os.path.dirname(os.path.abspath(__file__))
profilesDir = os.path.join(baseDir, "SavedProfiles");
modSettingsPath = os.path.join(
        userDir, "appData", "Local", "Larian Studios", "Baldur's Gate 3", "PlayerProfiles", "Public", "modsettings.lsx"
);

global language
language = "pt-BR"

def showMessage(title, message, parent=None):
    msgWindow = ctk.CTkToplevel()
    msgWindow.title(title)
    msgWindow.geometry("300x150")
    msgWindow.transient(parent)
    msgWindow.grab_set()  # bloqueia interação com outras janelas

    frame = ctk.CTkFrame(msgWindow, fg_color="transparent")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    label = ctk.CTkLabel(frame, text=message, wraplength=250, justify="center")
    label.pack(pady=20)

    okButton = ctk.CTkButton(frame, text="OK", command=msgWindow.destroy)
    okButton.pack(pady=10)

def onLanguageChange(new_lang):
    global locale, language
    global saveProfileButton, loadProfileButton

    locale = loadLocale(new_lang)
    language = new_lang
    saveProfileButton.configure(text=locale["save_profile_button"])
    loadProfileButton.configure(text=locale["load_profile_button"])

def loadLocale(language):
    with open(os.path.join(baseDir, "Settings", "Locale", "Locale.json"), "r", encoding="utf-8") as f:
        locales =  json.load(f);
    
    return locales.get(language, locales[language]);
    
def mainInterfaceLoop():
    global locale
    global saveProfileButton, loadProfileButton
    
    locale = loadLocale(language);
    
    window = ctk.CTk();
    window.title("BG3 Mods Profiles Manager")
    window.geometry("400x300");
    
    centerFrame = ctk.CTkFrame(window, fg_color="transparent")
    centerFrame.place(relx=0.5, rely=0.45, anchor="center") 
    
    saveProfileButton = ctk.CTkButton(centerFrame, text=locale["save_profile_button"], command = lambda: saveProfileInterface(window));
    saveProfileButton.pack(pady=10);
    
    loadProfileButton = ctk.CTkButton(centerFrame, text=locale["load_profile_button"], command = lambda: loadProfileInterface(window));
    loadProfileButton.pack(pady=10);
    
    combo = ctk.CTkComboBox(centerFrame, values=["pt-BR", "en-US"], command=onLanguageChange);
    combo.set(language)
    combo.configure(state="readonly")
    combo.pack(pady=10);
    
    window.mainloop();
    
def loadProfileInterface(window):
    locale = loadLocale(language);
    
    newWindow = ctk.CTkToplevel();
    newWindow.title(locale["load_profile_window_title"]);
    newWindow.geometry("400x300");
    newWindow.configure(bg_color="black")
    newWindow.grab_set()
    
    newWindow.transient(window);
    
    centerFrame = ctk.CTkFrame(newWindow, fg_color="transparent")
    centerFrame.place(relx=0.5, rely=0.45, anchor="center")
    
    combo = ctk.CTkComboBox(centerFrame, values=os.listdir(profilesDir));
    combo.configure(state="readonly")
    combo.pack(pady=40);
    
    loadButton = ctk.CTkButton(centerFrame, text=locale["load_button"], command=lambda: loadModsProfile(combo.get().replace(".lsx", "")));
    loadButton.place(relx=0.5, rely=0.85, anchor="center");
    
def loadModsProfile(profileName):
    shutil.copy(profilesDir + "/" + profileName + ".lsx", modSettingsPath);
    showMessage(locale["success"], locale["profile_loaded"])

def saveProfileInterface(window):
    locale = loadLocale(language);
    
    newWindow = ctk.CTkToplevel();
    newWindow.title(locale["save_profile_title"]);
    newWindow.geometry("400x300");
    newWindow.grab_set()
    
    newWindow.transient(window);
    
    centerFrame = ctk.CTkFrame(newWindow, fg_color="transparent")
    centerFrame.place(relx=0.5, rely=0.45, anchor="center")
    
    entry = ctk.CTkEntry(centerFrame, placeholder_text=locale["profile_name_placeholder"], width=200);
    entry.pack(pady=40);
    
    saveButton = ctk.CTkButton(centerFrame, text=locale["save_button"], command=lambda: saveCurrentModsProfile(entry.get()));
    saveButton.place(relx=0.5, rely=0.85, anchor="center");
    
def saveCurrentModsProfile(profileName):
    if not profileName:
        showMessage(locale["error"], locale["profile_name_empty"])
        return
    else:
        shutil.copy(modSettingsPath, profilesDir + "/" + profileName + ".lsx");
        showMessage(locale["success"], locale["profile_saved"])
    
if __name__ == "__main__":
    
    mainInterfaceLoop()