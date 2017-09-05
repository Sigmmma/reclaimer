from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

# Typing these up took FOREVER
game_data_input_functions = (
    'NULL', 'player settings menu update', 'unused',
    'playlist settings menu update', 'gametype select menu update',
    'multiplayer type menu update', 'solo level select update',
    'difficulty menu update', 'build number',  # textbox only for build_number
    'server list update', 'network pregame status update',
    'splitscreen pregame update', 'net/splitscreen prejoin players',
    'mp profile list update', 'wide 3 player profile list update',
    'player profile edit-select menu update',
    'player profile small menu update', 'game settings lists text update',
    'solo game objective text', 'color picker update',
    'game setings lists pic update', 'main menu fake animate',
    'mp level select update',
    'get active player profile name', 'get edit player profile name',
    'get edit game settings name', 'get active player profile color',
    'mp set textbox map name', 'mp set textbox game rules',
    'mp set textbox teams no teams', 'mp set textbox score limit',
    'mp set textbox score limit type', 'mp set bitmap for map',
    'mp set bitmap for ruleset', 'mp set textbox player count',
    'mp edit profile set rule text',
    'system link status check', 'mp game directions',
    'teams/no teams bitmap update', 'warn if diff will nuke saved game',
    'dim if no net cable', 'pause game set textbox inverted',
    'dim unless two controllers', 'controls update menu',
    'video menu update', 'gamespy screen update', 'common button bar update',
    'gamepad update menu', 'server settings update', 'audio menu update',
    'mp profile vehicles update', 'solo map list update', 'mp map list update',
    'gametype select list update', 'gametype edit list update',
    'load game list update', 'checking for updates',
    'direct ip connect update', 'network settings update',
    )
event_types = (
    'A button', 'B button', 'X button', 'Y button',
    'black button', 'white button', 'left trigger', 'right trigger',
    'dpad up', 'dpad down', 'dpad left', 'dpad right',
    'start button', 'back button', 'left thumb', 'right thumb',
    'left analog stick up', 'left analog stick down',
    'left analog stick left', 'left analog stick right',
    'right analog stick up', 'right analog stick down',
    'right analog stick left', 'right analog stick right',
    'created', 'deleted', 'get focus', 'lose focus',
    'left mouse', 'middle mouse', 'right mouse', 'double click',
    'custom activation', 'post render'
    )
event_functions = (
    'NULL', 'list goto next item', 'list goto previous item',
    'unused1', 'unused2', 'initialize sp level list solo',
    'initialize sp level list coop', 'dispose sp level list',
    'solo level set map', 'set difficulty', 'start new game',
    'pause game restart at checkpoint', 'pause game restart level',
    'pause game rturn to main menu', 'clear multiplayer player joins',
    'join controller to mp game', 'initialize net game server list',
    'start net game server', 'dispose net game server list',
    'shutdown net game server', 'net game join from server list',
    'split screen game initialize', 'coop game initialize',
    'main menu initialize', 'mp type menu initialize',
    'pick play stage for quick start', 'mp level list initialize',
    'mp level list dispose', 'mp level select', 'mp profiles list initialize',
    'mp profiles list dispose', 'mp profile set for game', 'swap player team',
    'net game join player', 'player profile list initialize',
    'player profile list dispose',
    'wide 3 player profile set for game', 'wide 1 player profile set for game',
    'mp profile begin editing', 'mp profile end editing',
    'mp profile set game engine', 'mp profile change name',
    'mp profile set ctf rules', 'mp profile set koth rules',
    'mp profile set slayer rules', 'mp profile set oddball rules',
    'mp profile set racing rules', 'mp profile set player options',
    'mp profile set item options', 'mp profile set indicator options',
    'mp profile init game engine', 'mp profile init name',
    'mp profile init ctf rules', 'mp profile init koth rules',
    'mp profile init slayer rules', 'mp profile init oddball rules',
    'mp profile init racing rules', 'mp profile init player options',
    'mp profile init item options', 'mp profile init indicator options',
    'mp profile save changes', 'color picker menu initialize',
    'color picker menu dispose', 'color picker select color',
    'player prof begin editing', 'player prof end editing',
    'player prof change name', 'player prof save changes',
    'player prof init control settings', 'player prof init adv ctrl settings',
    'player prof save control settings', 'player prof save adv ctrl settings',
    'mp game player quit', 'main menu switch to solo game',
    'request del player profile', 'request del playlist profile',
    'final del player profile', 'final del playlist profile',
    'cancel profile delete',
    'create and edit playlist profile', 'create and edit player profile',
    'net game speed start', 'net game delay start',
    'net server accept connection', 'net server defer start',
    'net server allow start', 'disable if no xdemos', 'run xdemos',
    'sp reset controller choices',
    'sp set p1 controller choices', 'sp set p2 controller choices',
    'error if no network connection', 'start server if none advertised',
    'net game unjoin player', 'close if not editing profile',
    'exit to xbox dashboard', 'new campaign chosen', 'new campaign decision',
    'pop history stack once', 'difficulty menu init', 'begin music fade out',
    'new game if no player profile', 'exit gracefully to xbox dashboard',
    'pause game invert pitch', 'start new coop game',
    'pause game invert spinner set', 'pause game invert spinner get',
    'main menu quit game',
    'mouse - emit ACCEPT event', 'mouse - emit BACK event',
    'mouse - emit DPAD LEFT event', 'mouse - emit DPAD RIGHT event',
    'mouse spinner 3wide click',
    'controls screen init', 'video screen init', 'controls begin binding',
    'gamespy screen init', 'gamespy screen dispose',
    'gamespy select header', 'gamespy select item', 'gamespy select button',
    'player prof init mouse set', 'player prof change mouse set',
    'player prof init audio set', 'player prof change audio set',
    'player prof change video set',
    'controls screen dispose', 'controls screen change set',
    'mouse emit X event', 'gamepad screen init', 'gamepad screen dispose',
    'gamepad screen change gamepads', 'gamepad screen select item',
    'mouse screen defaults', 'audio screen defaults', 'video screen defaults',
    'controls screen defaults', 'profile set edit begin',
    'profile manager delete', 'profile manager select',
    'gamespy dismiiss error', 'server settings init',
    'server set edit server name', 'server set edit server password', 
    'server set start game', 'video test dialog init',
    'video test dialog dispose', 'video test dialog accept',
    'gamespy dismiss filters', 'gamespy update filter settings',
    'gamespy dismiss back handler', 'mouse spinner 1wide click',
    'controls back handler', 'controls advanced launch', 'controls advanced ok',
    'mp pause menu open', 'mp game options open', 'mp choose team',
    'mp prof init vehicle options', 'mp prof save vehicle options',
    'single prev cl item active',
    'mp prof init teamplay options', 'mp prof save teamplay options',
    'mp game options choose', 'emit custom activation event',
    'player prof cancel audio set', 'player prof init network options',
    'player prof save network options', 'credits post render',
    'difficulty item select', 'credits initialize', 'credits dispose',
    'gamespy get patch', 'video screen dispose',
    'campaign menu init', 'campaign menu continue',
    'load game menu init', 'load game menu dispose', 'load game menu activated',
    'solo menu save checkpoint', 'mp type set mode',
    'checking for updates ok', 'checking for updates dismiss',
    'direct ip connect init', 'direct ip connect go', 'direct ip edit field',
    'network settings edit a port', 'network settings defaults',
    'load game menu delete request', 'load game menu delete finish'
    )

widget_bounds = QStruct("",
    SInt16("t"), SInt16("l"), SInt16("b"),  SInt16("r"),
    ORIENT='h', SIZE=8
    )

game_data_input = Struct("game data input",
    SEnum16("function", *game_data_input_functions),
    SIZE=36
    )

event_handler = Struct("event handler",
    Bool32('flags',
        "close current widget",
        "close other widget",
        "close all widgets",
        "open widget",
        "reload self",
        "reload other widget",
        "give focus to widget",
        "run function",
        "replace self with widget",
        "go back to previous widget",
        "run scenario script",
        "try to branch on failure",
        ),
    SEnum16("event type", *event_types),
    SEnum16("function", *event_functions),
    dependency("widget tag", "DeLa"),
    dependency("sound effect", "snd!"),
    ascii_str32("script"),
    SIZE=72
    )

s_and_r_reference = Struct("search and replace reference",
    ascii_str32("search string"),
    SEnum16("replace function",
        "NULL",
        "widgets controller",
        "build number",
        "pid",
        ),
    SIZE=34
    )

conditional_widget = Struct("conditional widget",
    dependency("widget tag", "DeLa"),
    ascii_str32("name"),  # UNUSED
    Bool32("flags",
        "load if event handler function fails",
        ),
    SInt16("custom controller index"),  # UNUSED
    SIZE=80
    )

child_widget = Struct("child widget",
    dependency("widget tag", "DeLa"),
    ascii_str32("name"),  # UNUSED
    Bool32("flags",
        "use custom controller index",
        ),
    SInt16("custom controller index"),
    SInt16("vertical offset"),
    SInt16("horizontal offset"),
    SIZE=80
    )

DeLa_body = Struct("tagdata",
    SEnum16("widget type",
        "container",
        "text box",
        "spinner list",
        "column list",
        "game model",  # not implemented
        "movie",  # not implemented
        "custom"  # not implemented
        ),
    SEnum16("controller index",
        "player 1",
        "player 2",
        "player 3",
        "player 4",
        "any player"
        ),
    ascii_str32("name"),
    QStruct("bounds", INCLUDE=widget_bounds),
    Bool32('flags',
        "pass unhandled events to focused child",
        "pause game time",
        "flash background bitmap",
        "dpad up/down tabs thru children",
        "dpad left/right tabs thru children",
        "dpad up/down tabs thru list items",
        "dpad left/right tabs thru list items",
        "dont focus a specific child widget",
        "pass unhandled events to all children",
        "return to main menu if no history",
        "always use tag controller index",
        "always use nifty render fx",
        "dont push history",
        "force handle mouse"
        ),
    SInt32("auto close time", SIDETIP="milliseconds"),
    SInt32("auto close fade time", SIDETIP="milliseconds"),
    dependency("background bitmap", "bitm"),

    reflexive("game data inputs", game_data_input, 64),
    reflexive("event handlers", event_handler, 32),
    reflexive("search and replace references",
              s_and_r_reference, 32, DYN_NAME_PATH='.search_string'),

    Pad(128),
    Struct("text box",
        dependency("text label unicode strings list", "ustr"),
        dependency("text font", "font"),
        QStruct("text color", INCLUDE=argb_float),
        SEnum16("justification",
            "left",
            "right",
            "center",
            ),
        # as weird as it sounds, these flags are off alignment by 2
        Bool32("flags",
            "editable",
            "password",
            "flashing",
            "dont do that weird focus test",
            ),
        BytesRaw("unknown2", SIZE=10, VISIBLE=False),

        FlSInt16("unknown3", VISIBLE=False),
        SInt16("string list index"),
        SInt16("horizontal offset"),
        SInt16("vertical offset")
        ),

    Pad(28),
    Struct("list items",
        Bool32("flags",
            "list items generated in code",
            "list items from string list tag",
            "list items only one tooltip",
            "list single preview no scroll"
            )
        ),

    Struct("spinner list",
        dependency("list header bitmap", "bitm"),
        dependency("list footer bitmap", "bitm"),
        QStruct("header bounds", INCLUDE=widget_bounds),
        QStruct("footer bounds", INCLUDE=widget_bounds)
        ),

    Pad(32),
    Struct("column list",
        dependency("extended description widget", "DeLa")
        ),

    Pad(288),
    reflexive("conditional widgets", conditional_widget, 32,
        DYN_NAME_PATH='.widget_tag.filepath'),

    Pad(256),
    reflexive("child widgets", child_widget, 32,
        DYN_NAME_PATH='.widget_tag.filepath'),

    SIZE=1004
    )

def get():
    return DeLa_def

DeLa_def = TagDef("DeLa",
    blam_header('DeLa'),
    DeLa_body,

    ext=".ui_widget_definition", endian=">", tag_cls=HekTag
    )
