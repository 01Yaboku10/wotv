import gamelogic as gl
import manu as menu
import saveloader as sl
import sound as sd
import google_sheet as gs

def main():
    print("Starting Whisper of The Void...")
    gs.get_creds()
    sl.load_characters("character_saves")
    foo = input("Continue and clear log:")
    sd.sound_play("menu_theme", 0.2, -1)
    gl.log_clear()
    menu.main_menu()

if __name__ == "__main__":
    main()
