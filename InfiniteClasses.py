import InfiniteApi

class Evolution_stat:
    def __init__(self):        
        self.current_value = 0.0
        self.session_value = 0.0
    
    def update(self, value):
        self.current_value = value
        self.session_value += value


class Game:
     
    def __init__(self, gamertag:str,init_session:bool=True):
        self.init = init_session
        self.changed = False

        self.id = "Empty"
        #game settings
        self.map_name = "Empty"
        self.game_playlist = "Empty"
        self.game_type = "Empty"

        #participation
        self.joined_in_progress = False

        #player part
        self.gamertag = gamertag

        #part stats
        self.kills = Evolution_stat()
        self.deaths = Evolution_stat()
        
        self.expected_kills = 0
        self.expected_deaths = 0

        self.assists = Evolution_stat()
        self.suicides = Evolution_stat()
        self.betrayals = Evolution_stat()
        self.max_killing_spree = 0
        self.kdr = 0

        self.damage_taken = 0
        self.damage_dealt = 0

        #weapon stats
        self.shots_fired = 0
        self.shots_hit = 0
        self.shots_missed = 0
        self.shots_accuracy = 0

        #head precision
        self.headshots = Evolution_stat()

        #progression
        self.xp = Evolution_stat()
        
        #game outcome
        self.outcome = "raw"

        #game duration
        self.human = ""

    def update(self):
        game = InfiniteApi.get_last_game_stat(self.gamertag)
        if self.init:
            self.id                     = game["id"]
            self.init                   = False
        self.changed = self.id != game["id"]
        if  self.changed:
            self.id                      = game["id"]
            self.map_name                = game["details"]["map"]["name"]
            self.game_playlist           = game["details"]["playlist"]["name"]
            self.game_type               = game["details"]["ugcgamevariant"]["name"]
            self.joined_in_progress      = game["player"]["participation"]["joined_in_progress"]
            self.kills.update(game["player"]["stats"]["core"]["summary"]["kills"])
            self.deaths.update(game["player"]["stats"]["core"]["summary"]["deaths"])
            self.assists.update(game["player"]["stats"]["core"]["summary"]["assists"])
            self.suicides.update(game["player"]["stats"]["core"]["summary"]["suicides"])
            self.betrayals.update(game["player"]["stats"]["core"]["summary"]["betrayals"])
            self.max_killing_spree       = game["player"]["stats"]["core"]["summary"]["max_killing_spree"]
            self.kdr                     = game["player"]["stats"]["core"]["kdr"]
            self.damage_taken            = game["player"]["stats"]["core"]["damage"]["taken"]
            self.damage_dealt            = game["player"]["stats"]["core"]["damage"]["dealt"]
            self.shots_fired             = game["player"]["stats"]["core"]["shots"]["fired"]
            self.shots_hit               = game["player"]["stats"]["core"]["shots"]["hit"]
            self.shots_missed            = game["player"]["stats"]["core"]["shots"]["missed"]
            self.shots_accuracy          = game["player"]["stats"]["core"]["shots"]["accuracy"]
            self.headshots.update(game["player"]["stats"]["core"]["breakdown"]["kills"]["headshots"])
            self.xp.update(game["player"]["stats"]["core"]["scores"]["personal"])
            self.outcome                 = game["player"]["outcome"]
            self.human                   = game["playable_duration"]["human"]
            self.expected_kills          = game["player"]["performances"]["kills"]["expected"]
            self.expected_deaths         = game["player"]["performances"]["deaths"]["expected"]

        
    def __str__(self):
        return f"""
        ```m
        ============ game-infos ============
        id: {self.id}
        name: {self.map_name}
        playlist: {self.game_playlist}
        --->mode: {self.game_type}

        current player: {self.gamertag}
        
        ============ statistics ============        
        kills   : {self.kills.session_value:,.0f} (+{self.kills.current_value})  | kdr: {self.kdr:,.02f}
        deaths  : {self.deaths.session_value:,.0f} (+{self.deaths.current_value})
        assists : {self.assists.current_value:,.0f} (+{self.assists.current_value})
        --->expected kills : {self.expected_kills:.2f}
        --->expected deaths: {self.expected_deaths:.2f}

        max killing spree: {self.max_killing_spree:,.0f}
        
        suicides: {self.suicides.session_value:,.0f} (+{self.suicides.current_value})
        betrayals: {self.betrayals.session_value:,.0f} (+{self.betrayals.current_value})
        
        damage taken: {self.damage_taken:,.0f}
        damage dealt: {self.damage_dealt:,.0f}
        
        ============= weapons =============
        shots fired: {self.shots_fired:,.0f}
        shots hit: {self.shots_hit:,.0f}
        shots missed: {self.shots_missed:,.0f}
        shots accuracy: {self.shots_accuracy:,.2f}%

        headshots: {self.headshots.session_value:,.0f} (+{self.headshots.current_value})
        
        =========== progression ===========
        total experiences: {self.xp.session_value:,.0f} xp (+{self.xp.current_value:,.0f} xp)
        
        ============== bonus ==============
        game had already started: {self.joined_in_progress}
        duration: {self.human}
        outcome: {self.outcome}
        ```
        """
    

    
class Global:
    def __init__(self, gamertag:str):        
        self.gamertag = gamertag

        game = InfiniteApi.get_stat_player(self.gamertag)

        self.kills = game["data"]["stats"]["core"]["summary"]["kills"]
        self.deaths = game["data"]["stats"]["core"]["summary"]["deaths"]
        self.assists = game["data"]["stats"]["core"]["summary"]["assists"]
        self.betrayals = game["data"]["stats"]["core"]["summary"]["betrayals"]
        self.suicides = game["data"]["stats"]["core"]["summary"]["suicides"]
        self.max_killing_spree = game["data"]["stats"]["core"]["summary"]["max_killing_spree"]

        self.damage_taken = game["data"]["stats"]["core"]["damage"]["taken"]
        self.damage_dealt = game["data"]["stats"]["core"]["damage"]["dealt"]        
        self.accuracy = game["data"]["stats"]["core"]["shots"]["accuracy"]

        self.rounds_won = game["data"]["stats"]["core"]["rounds"]["won"]
        self.rounds_lost = game["data"]["stats"]["core"]["rounds"]["lost"]
        self.rounds_tie = game["data"]["stats"]["core"]["rounds"]["tied"]

        self.breakdown_kills_melee = game["data"]["stats"]["core"]["breakdown"]["kills"]["melee"]
        self.breakdown_kills_grenades = game["data"]["stats"]["core"]["breakdown"]["kills"]["grenades"]
        self.breakdown_kills_headshots = game["data"]["stats"]["core"]["breakdown"]["kills"]["headshots"]
        self.breakdown_kills_power_weapons = game["data"]["stats"]["core"]["breakdown"]["kills"]["power_weapons"]
        self.breakdown_kills_sticks = game["data"]["stats"]["core"]["breakdown"]["kills"]["sticks"]
        self.breakdown_kills_assassinations = game["data"]["stats"]["core"]["breakdown"]["kills"]["assassinations"]
        self.breakdown_kills_vehicules_splatters = game["data"]["stats"]["core"]["breakdown"]["kills"]["vehicles"]["splatters"]
        self.breakdown_kills_miscellaneous_repulsor = game["data"]["stats"]["core"]["breakdown"]["kills"]["miscellaneous"]["repulsor"]
        self.breakdown_kills_miscellaneous_fusion_coil = game["data"]["stats"]["core"]["breakdown"]["kills"]["miscellaneous"]["fusion_coils"]

        self.kdr = game["data"]["stats"]["core"]["kdr"]
        self.scores_xp = game["data"]["stats"]["core"]["scores"]["personal"]

        self.time_played_human = game["data"]["time_played"]["human"]

    def __str__(self):
        return f"""
        ```m
        ============= Player-info =============
        gamertag: {self.gamertag}
        
        ========== kills statistics ===========
        kills   : {self.kills:,} | kdr : {self.kdr:,.2f}
        deaths  : {self.deaths:,}
        assists : {self.assists:,}

        betrayals: {self.betrayals:,}
        suicides : {self.suicides:,}

        max killing spree: {self.max_killing_spree:,}

        ========== damage statistics ==========
        damage taken: {self.damage_taken:,}
        damage dealt: {self.damage_dealt:,}
        --->accuracy: {self.accuracy:.2f} %

        ========== rounds statistics ==========
        rounds won : {self.rounds_won:,}
        rounds lost: {self.rounds_lost:,}
        rounds tie : {self.rounds_tie:,}

        ========== kills breakdown ============
        melee kills        : {self.breakdown_kills_melee:,}
        grenade kills      : {self.breakdown_kills_grenades:,}
        headshots          : {self.breakdown_kills_headshots:,}
        power weapons      : {self.breakdown_kills_power_weapons:,}
        sticks             : {self.breakdown_kills_sticks:,}
        assassinations     : {self.breakdown_kills_assassinations:,}
        vehicule splatters : {self.breakdown_kills_vehicules_splatters:,}
        repulsor           : {self.breakdown_kills_miscellaneous_repulsor:,}
        fusion coil        : {self.breakdown_kills_miscellaneous_fusion_coil:,}
        
        total experiences: {self.scores_xp:,} xp
        time played: {self.time_played_human}
        ```
        """
    



def dir_path():
    return "C:/Users/Maelm/Documents/halo_medals"


if __name__ == "__main__":
    pass
    g = Global("IceCurim")
    print(str(g))