import gamelogic as gl
import manu as menu
import saveloader as sl
import sound as sd
import google_sheet as gs

def main():
    gl.print_debugg("DEBUGG", "Starting game...")
    gs.get_creds()
    sl.load_characters("character_saves")
    foo = input("Continue and clear log:")
    sd.sound_play("menu_theme", 0.2, -1)
    gl.log_clear()
    print(
" __      __       .__                                  __                                                              \n"
"/  \    /  \ ____ |  |   ____  ____   _____   ____   _/  |_  ____                                                      \n"
"\   \/\/   // __ \|  | _/ ___\/  _ \ /     \_/ __ \  \   __\/  _ \                                                     \n"
" \        /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/   |  | (  <_> )                                                    \n"
"  \__/\  /  \___  >____/\___  >____/|__|_|  /\___  >  |__|  \____/                                                     \n"
"       \/       \/          \/            \/     \/                                                                    \n"
" __      __.__    .__                                      _____  ___________.__             ____   ____    .__    .___\n"
"/  \    /  \  |__ |__| ____________   ___________    _____/ ____\ \__    ___/|  |__   ____   \   \ /   /___ |__| __| _/\n"
"\   \/\/   /  |  \|  |/  ___/\____ \_/ __ \_  __ \  /  _ \   __\    |    |   |  |  \_/ __ \   \   Y   /  _ \|  |/ __ | \n"
" \        /|   Y  \  |\___ \ |  |_> >  ___/|  | \/ (  <_> )  |      |    |   |   Y  \  ___/    \     (  <_> )  / /_/ | \n"
"  \__/\  / |___|  /__/____  >|   __/ \___  >__|     \____/|__|      |____|   |___|  /\___  >    \___/ \____/|__\____ | \n"
"       \/       \/        \/ |__|        \/                                       \/     \/                         \/ \n")
    menu.main_menu()

if __name__ == "__main__":
    main()
