import gamelogic as gl
import manu as menu
import saveloader

def main():
    print("Starting Whisper of The Void...")
    saveloader.load_characters("character_saves")
    foo = input("Continue and clear log:")
    gl.log_clear()
    menu.main_menu()

main()