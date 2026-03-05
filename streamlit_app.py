"""
Testament TCG — Card Generation Engine
Streamlit Web App (self-contained, no external deps beyond streamlit)
"""

import random
import re
from datetime import datetime
import streamlit as st

st.set_page_config(
    page_title="Testament TCG",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ────────────────────────────────────────────────────────────────────────────────
# DATA — FACTIONS
# ────────────────────────────────────────────────────────────────────────────────

FACTIONS = {
    "Celestial Host": {
        "symbol": "✦", "faith_color": "white",
        "adjectives": ["divine", "holy", "radiant", "blessed", "eternal", "sacred", "hallowed", "celestial"],
        "servant_nouns": ["Angel", "Archangel", "Seraph", "Saint", "Paladin", "Guardian", "Warden", "Champion"],
        "servant_types": ["Angel", "Angel / Archangel", "Angel / Seraph", "Spirit / Saint", "Human / Paladin"],
        "proper_names": ["Uriel", "Michael", "Gabriel", "Raphael", "Jophiel", "Haniel", "Zadkiel", "Chamuel"],
        "prayer_names": ["Benediction", "Consecration", "Absolution", "Intercession", "Holy Writ", "Divine Grace"],
        "miracle_names": ["Heavenly Intervention", "Divine Parry", "Flash of Grace", "Angelic Response", "Holy Shield"],
        "covenant_names": ["Eternal Vigil", "Covenant of Light", "Sacred Pact", "Heaven's Promise", "The Holy Oath"],
        "relic_names": ["Sword of Purifying Flame", "Heaven's Shield", "Seraph's Feather", "Sacred Chalice", "Aureate Crown"],
        "shrine_names": ["Heaven's Gate Shrine", "Holy Sanctuary", "Cathedral of Light", "Sacred Grove", "Celestial Altar"],
        "trap_names": ["Heaven's Judgment", "Divine Retribution", "Angel's Warning", "Sacred Ward", "Holy Counter"],
        "keywords": ["Consecrated", "Blessed", "Herald", "Radiant", "Divine Shield", "Vigilance", "Ascend"],
        "triggered_effects": [
            "When {NAME} enters: Exile target Fallen or Demonic Servant until {NAME} leaves play.",
            "When {NAME} enters: You gain 2000 Life Points.",
            "When {NAME} is destroyed: Return target Angel from your Graveyard to your hand.",
            "Whenever you cast a Prayer: {NAME} gets a +100 ATK counter.",
            "When {NAME} enters: Create a 1000/1000 Seraph token with Consecrated.",
            "At the beginning of your upkeep: Remove 1 Curse counter from a Servant you control.",
            "When {NAME} enters: Search your deck for a Shrine and put it into play.",
        ],
        "activated_effects": [
            "{2}{✦}: Destroy target Servant with ATK 2000 or less.",
            "{✦}: Prevent 1000 damage to a Servant you control this turn.",
            "{Tap}: Give target Servant Consecrated until end of turn.",
        ],
        "prayer_effects": [
            "Destroy target Fallen Dominion Servant. Gain life equal to its ATK / 100.",
            "Draw 2 cards. You gain 1500 Life Points.",
            "All your Servants gain +500 ATK and +500 DEF until end of turn.",
            "Return Servants from your Graveyard with ATK 1500 or less to your hand.",
            "Exile all Servants in all Graveyards. Gain 300 Life per Servant exiled.",
        ],
        "miracle_effects": [
            "Counter target spell or activated ability.",
            "Target Servant gains Consecrated until end of turn. It cannot be destroyed this turn.",
            "Prevent all combat damage from target Servant this turn.",
            "Exile target Servant. Its controller gains 1000 Life Points.",
        ],
        "covenant_effects": [
            "All Celestial Host Servants you control get +300 ATK and +300 DEF.",
            "Whenever a Servant enters under your control, you gain 500 Life Points.",
            "Fallen Dominion Servants lose 500 ATK while on the battlefield.",
            "Your Servants cannot be targeted by your opponent's effects.",
        ],
        "relic_effects": [
            "Equipped Servant gets +600 ATK / +400 DEF. When it destroys a Servant, exile that Servant.",
            "Equipped Servant gains Consecrated and Vigilance.",
            "Once per turn: Prevent 800 damage to equipped Servant.",
            "{2}: Attach this Relic to target Servant you control.",
        ],
        "shrine_effects": [
            "{Tap}: Add {✦} to your Faith pool.",
            "{Tap}: Add {✦}. If you control 5+ Shrines, add {✦}{✦} instead.",
            "{Tap}: Add {✦}. Once per turn, pay {✦}: Draw 1 card.",
        ],
        "trap_effects": [
            "When your opponent declares an attack: Destroy the attacking Servant.",
            "When a Fallen Dominion Servant is summoned: Banish it instead.",
            "When your opponent activates a Prayer or Miracle: Negate it. Gain 500 Life Points.",
        ],
        "flavor_quotes": [
            '"By the Lord\'s command, none shall pass who bear the mark of sin."',
            '"We do not fight with hatred — we fight with absolute love for what is right."',
            '"The gates of heaven are not locked to keep darkness out. They are open to welcome the faithful in."',
            '"I have seen the end of all things. This is not it."',
            '"Even the fallen were once radiant. That is why we grieve as we strike them down."',
            '"Heaven\'s army does not march to conquer. It marches to protect."',
            '"In the light of the eternal, all shadows are temporary."',
            '"We are the shield upon which corruption breaks."',
        ],
        "art_style": "baroque religious painting, Raphael/Michelangelo influence, gold/white/ivory, divine light rays",
    },

    "Fallen Dominion": {
        "symbol": "☽", "faith_color": "black",
        "adjectives": ["fallen", "corrupted", "sinful", "dark", "wicked", "infernal", "damned", "shadowed"],
        "servant_nouns": ["Demon", "Devil", "Shade", "Wraith", "Archfiend", "Sin", "Betrayer", "Corruptor"],
        "servant_types": ["Demon / Fiend", "Fallen Angel / Demon", "Spirit / Shade", "Human / Sinner", "Beast / Hell-Spawn"],
        "proper_names": ["Malphas", "Vassago", "Asmodeus", "Belial", "Bael", "Agares", "Valac", "Paimon"],
        "prayer_names": ["Blood Rite", "Dark Pact", "Infernal Prayer", "Hellfire Litany", "Cursed Blessing"],
        "miracle_names": ["Dark Intervention", "Shadow Step", "Infernal Response", "Soul Steal", "Void Strike"],
        "covenant_names": ["Pact of Blood", "Infernal Covenant", "Devil's Bargain", "Eternal Damnation", "Shadow Oath"],
        "relic_names": ["Soul Chain", "Corruption Sigil", "Hellfire Brand", "Damnation Scepter", "Void Amulet"],
        "shrine_names": ["Altar of Sacrifice", "Infernal Gate", "Void Rift", "Hellfire Shrine", "Dark Sanctum"],
        "trap_names": ["Soul Trap", "Infernal Snare", "Dark Counter", "Hell's Ambush", "Corruption Trigger"],
        "keywords": ["Invoke", "Corrupted", "Soul Bind", "Sacrifice", "Fallen", "Wrath", "Zealot"],
        "triggered_effects": [
            "When {NAME} is destroyed: Deal 1500 damage to your opponent.",
            "When {NAME} is destroyed: Pay {☽} to Special Summon it immediately.",
            "When {NAME} enters: Target opponent discards 1 card.",
            "Whenever you sacrifice a Servant: {NAME} gains +200 ATK until end of turn.",
            "When {NAME} is destroyed: Add 1 Fallen Dominion Servant from your deck to your hand.",
            "At the start of your turn: Add {☽} for each Servant in your Graveyard (max 3).",
            "When {NAME} enters: Destroy target Servant with DEF 1500 or less.",
        ],
        "activated_effects": [
            "{☽}: Sacrifice a Servant. Draw 2 cards.",
            "{2}{☽}: Destroy target Servant. Your opponent gains control of a card in your hand.",
            "Sacrifice {NAME}: Add {☽}{☽}{☽} to your Faith pool.",
        ],
        "prayer_effects": [
            "Destroy all Servants with ATK 2500 or less. Gain 300 Life per Servant destroyed.",
            "Target opponent discards 2 cards at random.",
            "Exile target Servant and return it under your control at end of turn, then destroy it.",
            "Search your deck for any Fallen Dominion card. Lose 1000 Life Points.",
        ],
        "miracle_effects": [
            "Counter target Prayer. Your opponent discards a card.",
            "Target Servant gains +2000 ATK until end of turn. Destroy it at end of turn.",
            "Sacrifice a Servant: Counter target spell or effect.",
            "Exile target Servant. Gain Life Points equal to its ATK / 100.",
        ],
        "covenant_effects": [
            "At the start of your opponent's turn, they lose 500 Life Points.",
            "Whenever a Servant is destroyed anywhere, you may draw 1 card.",
            "All your Fallen Dominion Servants gain +500 ATK.",
            "Your opponent's Servants cannot grant life to their controller.",
        ],
        "relic_effects": [
            "Equipped Servant gains +800 ATK. At start of your turn, it loses 200 DEF.",
            "Equipped Servant gains Soul Bind and Wrath.",
            "Once per turn: Equipped Servant can attack twice during the Battle Phase.",
            "{☽}: Attach this Relic to any Servant (yours or opponent's).",
        ],
        "shrine_effects": [
            "{Tap}: Add {☽} to your Faith pool.",
            "{Tap}: Add {☽}. You may sacrifice a Servant: Add {☽}{☽} instead.",
            "{Tap}: Add {☽}. Lose 500 Life Points: Add {☽}{☽} instead.",
        ],
        "trap_effects": [
            "When your opponent Special Summons a Servant: Destroy it. Deal 1000 damage.",
            "When your Life Points drop to 3000 or less: Deal 3000 damage to your opponent.",
            "When your opponent activates an effect: Negate it. That player discards 2 cards.",
        ],
        "flavor_quotes": [
            '"Power without limit requires sacrifice without limit."',
            '"We did not fall. We chose to fly in a different direction."',
            '"The only sin is weakness."',
            '"Heaven rejected me. So I built something far more interesting."',
            '"Every soul has a price. The question is: who names it?"',
            '"I was made of light. Now I am made of purpose."',
            '"Darkness does not destroy the light. It reveals what it was hiding."',
            '"The fallen do not despair. They remember."',
        ],
        "art_style": "gothic dark fantasy, twisted beauty, crimson/black/purple, hellfire glow, Gustave Doré influence",
    },

    "Prophetic Order": {
        "symbol": "📜", "faith_color": "blue",
        "adjectives": ["prophetic", "ancient", "wise", "arcane", "foreseen", "hidden", "inscribed", "revealed"],
        "servant_nouns": ["Prophet", "Apostle", "Scribe", "Sage", "Oracle", "Seer", "Scholar", "Visionary"],
        "servant_types": ["Human / Prophet", "Human / Apostle", "Spirit / Oracle", "Human / Sage", "Construct / Golem of Knowledge"],
        "proper_names": ["Eliyah", "Petrus", "Nael", "Delphis", "Morrigan", "Aramis", "Ezekias", "Devorah"],
        "prayer_names": ["Forbidden Revelation", "Ancient Decree", "Prophetic Mandate", "The Written Word", "Divine Record"],
        "miracle_names": ["Foreseen Counter", "Prophetic Denial", "The Foretold End", "Written in Stone", "Ancient Negation"],
        "covenant_names": ["The Eternal Record", "Covenant of Truth", "Scroll of Fate", "Prophetic Compact", "The Great Library"],
        "relic_names": ["Scroll of Omniscience", "The Prophet's Staff", "Tome of the Foretold", "Astrolabe of Stars", "Quill of Fate"],
        "shrine_names": ["Oracle's Chamber", "Library of the Ages", "Astral Observatory", "The Sacred Archive", "Temple of Revelation"],
        "trap_names": ["Prophetic Counter", "The Foretold Trap", "Ancient Ward", "Scribe's Snare", "Written Refusal"],
        "keywords": ["Prophesy", "Flash", "Vigilance", "Herald", "Martyr", "Eternal"],
        "triggered_effects": [
            "When {NAME} enters: Look at your opponent's hand. One card cannot be played until your next turn.",
            "Whenever you cast a Prayer or Miracle: Look at top 2 cards of your deck, keep 1.",
            "When {NAME} enters: Draw 2 cards.",
            "At beginning of your upkeep: Draw 1 card. If you have 10+ cards in hand, draw 2 instead.",
            "Whenever your opponent casts a spell: You may draw 1 card.",
            "When {NAME} is destroyed: Counter target spell or effect.",
            "When {NAME} enters: Search your deck for a Miracle and add it to your hand.",
        ],
        "activated_effects": [
            "{1}{📜}: Counter target Prayer or Miracle.",
            "{2}: Look at top 3 cards of any player's deck. Rearrange them.",
            "{📜}: Draw 1 card, then discard 1 card.",
        ],
        "prayer_effects": [
            "Look at the top 7 cards of your deck. Put 2 in hand, rest back in any order.",
            "Target opponent reveals their hand. Choose cards that cannot be played until their next turn.",
            "Mill half of your opponent's deck to their Graveyard.",
            "Draw 4 cards. Discard 2 cards.",
        ],
        "miracle_effects": [
            "Counter target spell. Its controller draws 1 card.",
            "Until your next turn, spells cost {2} more for your opponent.",
            "Counter target activated ability. Copy it and apply it to yourself instead.",
            "Target Servant cannot attack or use abilities until your next turn.",
        ],
        "covenant_effects": [
            "Prayers and Miracles you cast cost {1} less (minimum {1}).",
            "Your hand size maximum is 10 instead of 7.",
            "At the start of your turn, look at the top card of your deck. You may bottom it.",
            "Whenever your opponent draws a card, pay {1}: Draw a card.",
        ],
        "relic_effects": [
            "Equipped Servant gains Prophesy and 'When it attacks, draw 1 card'.",
            "Equipped Servant gains +400 ATK and Flash.",
            "Once per turn: Equipped Servant may look at the top card of any player's deck.",
            "{📜}: Move equipped Relic to another Servant you control.",
        ],
        "shrine_effects": [
            "{Tap}: Add {📜} to your Faith pool.",
            "{Tap}: Add {📜}. If not your first shrine tapped this turn, draw 1 card.",
            "{Tap}: Add {📜}. Once per turn, {📜}: Counter target activated ability.",
        ],
        "trap_effects": [
            "When your opponent declares an attack: Draw 2 cards. End the Battle Phase.",
            "When your opponent casts a Prayer or Miracle: Counter it. Opponent discards a card.",
            "When your opponent plays a Servant: Look at their hand. Put 1 card on top of their deck.",
        ],
        "flavor_quotes": [
            '"I have seen where this path leads. That is why I stand here."',
            '"The fool acts. The wise foresees, then acts."',
            '"Every ending was written long before it arrived."',
            '"We do not predict the future. We read what was always written."',
            '"Knowledge is not power. Knowledge is the only power. Everything else is its shadow."',
            '"The book was not written to be understood. It was written to be studied — forever."',
            '"A word unspoken cannot be countered. A word spoken cannot be unspoken."',
            '"I have no enemies. Only subjects of prophecy who have not yet arrived at their appointed place."',
        ],
        "art_style": "illuminated manuscript, ancient scrollwork, earth tones/deep blue, candlelight, Persian miniature influence",
    },

    "Ancient Pantheon": {
        "symbol": "⚡", "faith_color": "red",
        "adjectives": ["ancient", "olympian", "divine", "mythic", "titanic", "primordial", "eternal", "godly"],
        "servant_nouns": ["God", "Titan", "Demi-God", "Champion", "Deity", "Dragon", "Colossus", "Behemoth"],
        "servant_types": ["God / Olympian", "God / Aesir", "God / Ennead", "Mythic / Dragon", "Titan / Giant", "God / Teteo"],
        "proper_names": ["Zeus", "Odin", "Ra", "Quetzalcoatl", "Ares", "Thor", "Anubis", "Tlaloc"],
        "prayer_names": ["Divine Wrath", "God's Decree", "Olympian Rite", "Sacred Destruction", "The Pantheon's Will"],
        "miracle_names": ["Lightning Strike", "Thunderbolt Response", "God's Fury", "Divine Smite", "Titan's Roar"],
        "covenant_names": ["The Olympian Accord", "Ragnarok Pact", "The Eternal Pantheon", "God's Domain", "Divine Supremacy"],
        "relic_names": ["Mjolnir, God-Hammer", "Aegis, Divine Shield", "Ankh of Eternity", "Trident of the Deep", "Blade of Ares"],
        "shrine_names": ["Mount Olympus", "Yggdrasil Root", "Temple of Ra", "Pyramid of the Sun", "Valhalla Gate"],
        "trap_names": ["God's Punishment", "Olympian Trap", "Divine Retribution", "Pantheon Counter", "Titan's Snare"],
        "keywords": ["Smite", "Zealot", "Wrath", "Divinity", "Transcend", "Banish"],
        "triggered_effects": [
            "When {NAME} enters: Deal 2000 damage to target Servant.",
            "When {NAME} is destroyed: Destroy all Servants with ATK less than {NAME}'s ATK.",
            "Whenever {NAME} attacks: Deal 500 damage to target Servant or player.",
            "At the beginning of your Battle Phase: {NAME} gains +500 ATK until end of turn.",
            "When {NAME} enters: All opponent's Servants lose 500 ATK until end of turn.",
            "Whenever a Servant is destroyed anywhere: {NAME} gets a +100 ATK counter.",
            "When {NAME} enters: Destroy all non-God Servants with ATK 2000 or less.",
        ],
        "activated_effects": [
            "{⚡}{⚡}: {NAME} gains +1000 ATK until end of turn. It must attack if able.",
            "{2}{⚡}: Deal 1500 damage to target Servant.",
            "{⚡}: {NAME} may attack again this Battle Phase.",
        ],
        "prayer_effects": [
            "Deal 3000 damage to all Servants. Each destroyed Servant deals 300 damage to its controller.",
            "Destroy all non-God Servants on the battlefield.",
            "Target Servant gains +2000 ATK until end of turn. If it destroys a Servant, destroy 1 more.",
            "Deal 2500 damage to target Servant or player.",
        ],
        "miracle_effects": [
            "Target Servant gets -3000 ATK until end of turn.",
            "Deal 2000 damage to target Servant. If destroyed, deal 1000 to its controller.",
            "Target Servant cannot attack or block this turn.",
            "Counter target Prayer or Miracle. Deal 1000 damage to its controller.",
        ],
        "covenant_effects": [
            "Whenever a Servant you control deals damage, it deals 200 more.",
            "At the start of your Battle Phase: All your Servants gain +300 ATK until end of turn.",
            "God-type Servants cannot be destroyed by non-God effects.",
            "Opponent's Servants get -200 ATK for each God you control.",
        ],
        "relic_effects": [
            "Equipped Servant gets +1000 ATK. When it attacks, deal 300 damage to your opponent.",
            "Equipped Servant gains Smite and Zealot.",
            "Once per turn: Equipped Servant may attack directly, ignoring blockers.",
            "{⚡}: Attach this Relic to any Servant, including opponent's.",
        ],
        "shrine_effects": [
            "{Tap}: Add {⚡} to your Faith pool.",
            "{Tap}: Add {⚡}. If you control a God-type Servant, add {⚡}{⚡} instead.",
            "{Tap}: Add {⚡}. Once per turn, deal 200 damage to target Servant or player.",
        ],
        "trap_effects": [
            "When your opponent attacks with 3+ Servants: Destroy all attacking Servants.",
            "When your opponent activates an effect: Deal 1000 damage to them and negate the effect.",
            "When your Life Points drop below 4000: All your Servants gain +1000 ATK until end of turn.",
        ],
        "flavor_quotes": [
            '"I am not worshipped because I am kind. I am worshipped because I am inevitable."',
            '"The thunder does not negotiate."',
            '"Mortals name the stars after us. We named ourselves after nothing — we simply are."',
            '"Every civilization that forgets the old gods eventually learns why they should not have."',
            '"I have watched worlds end. This one is no different."',
            '"Legends are just memories that outlive the ones who made them."',
            '"The gods do not die. We transform."',
            '"Do not pray to me for mercy. Pray to me for victory. Those I can give."',
        ],
        "art_style": "epic mythology painting, dramatic chiaroscuro, bold saturated colors, David/Bouguereau influence, monumental",
    },

    "Dharmic Path": {
        "symbol": "☸", "faith_color": "green",
        "adjectives": ["enlightened", "serene", "balanced", "dharmic", "compassionate", "eternal", "pure", "harmonious"],
        "servant_nouns": ["Monk", "Deva", "Bodhisattva", "Master", "Sage", "Spirit", "Lotus-Born", "Ascetic"],
        "servant_types": ["Human / Monk", "Spirit / Deva", "Spirit / Bodhisattva", "God / Deva", "Human / Sage"],
        "proper_names": ["Avalokita", "Brahma", "Wukong", "Amaterasu", "Ryujin", "Siddhi", "Laozi", "Durga"],
        "prayer_names": ["Dharma Wheel", "Sacred Breath", "The Middle Path", "Lotus Sutra", "Path of Balance"],
        "miracle_names": ["Karmic Response", "Balance Restored", "Serene Counter", "The Dharmic Shield", "Lotus Defense"],
        "covenant_names": ["The Dharmic Law", "Covenant of Balance", "The Eternal Path", "Sacred Harmony", "The Unbroken Circle"],
        "relic_names": ["Prayer Beads of Eternity", "Lotus Throne", "Staff of Dharma", "Sacred Bell", "Bodhi Leaf"],
        "shrine_names": ["Temple of Lotus", "Sacred Mountain Path", "River of Karma", "Zen Garden", "Bodhi Tree Grove"],
        "trap_names": ["Karmic Reversal", "The Dharmic Trap", "Balance Counter", "Serene Snare", "Lotus Rebuff"],
        "keywords": ["Meditate", "Karmic", "Pilgrimage", "Dharmic", "Transcend", "Eternal", "Vigilance"],
        "triggered_effects": [
            "When {NAME} enters: You gain 2000 Life Points.",
            "Whenever an opponent's effect would deal damage to you: Prevent it. Gain that much Life instead.",
            "At the beginning of your upkeep: Gain 1000 Life Points and add {☸} to your Faith pool.",
            "When {NAME} enters: All your Servants gain +200 DEF until end of turn.",
            "Whenever you gain life: {NAME} gets a Karma counter. At 5 counters, draw 1 card.",
            "When {NAME} is destroyed: Return it to your hand. You gain 500 Life Points.",
            "When {NAME} enters: Search your deck for a Shrine. Put it into play.",
        ],
        "activated_effects": [
            "{☸}: Prevent 1500 damage to a Servant or player you control this turn.",
            "{1}{☸}: Remove all negative counters from target Servant you control.",
            "{☸}{☸}: {NAME} gains Transcend until end of turn. It cannot be targeted.",
        ],
        "prayer_effects": [
            "Gain 3000 Life Points. Draw cards equal to your Servants with Karma counters.",
            "All Servants gain +0/+1000 DEF until end of turn. They cannot be destroyed in combat.",
            "Return Servants from your Graveyard with DEF 2000+ to the battlefield.",
            "Target player shuffles their Graveyard into their deck. Lose 1000 Life Points.",
        ],
        "miracle_effects": [
            "Convert up to 2000 damage from a source to Life Points you gain instead.",
            "Target Servant gains +0/+2000 DEF until end of turn.",
            "Until your next turn, prevent the next damage each opponent would deal.",
            "Counter target spell that would deal damage. Gain Life Points equal to that damage.",
        ],
        "covenant_effects": [
            "At start of your turn, gain 500 Life Points if you have more life than your opponent.",
            "All your Servants in Defense Position gain +1000 DEF.",
            "Whenever you gain life, put a Karma counter on this. At 10 counters, you win the game.",
            "Damage that would be dealt to you is reduced by 300.",
        ],
        "relic_effects": [
            "Equipped Servant gains Meditate and +1500 DEF.",
            "Equipped Servant: Whenever it survives combat, you gain 500 Life Points.",
            "Once per turn: Equipped Servant may switch to Defense Position without tapping.",
            "{☸}: Move this Relic to another Servant. You gain 300 Life Points.",
        ],
        "shrine_effects": [
            "{Tap}: Add {☸} to your Faith pool.",
            "{Tap}: Add {☸}. If your Life Points exceed 6000, gain 300 Life Points.",
            "{Tap}: Add {☸}. Remove 1 Karma counter from any card: draw 1 card.",
        ],
        "trap_effects": [
            "When your opponent attacks: Convert all combat damage you would take to Life Points gained.",
            "When your Life Points would drop below 2000: Prevent that damage and gain 2000 Life Points.",
            "When your opponent activates an effect: Negate it. You gain 1000 Life Points.",
        ],
        "flavor_quotes": [
            '"True strength is not destroying your enemy. True strength is not needing to."',
            '"The river does not fight the stone. It flows around it — and the stone wears away."',
            '"Peace is not the absence of conflict. It is the transcendence of it."',
            '"Every breath is a prayer. Every moment, an offering."',
            '"I have nothing to prove to those who measure with the wrong scales."',
            '"The lotus blooms in muddy water. So do we."',
            '"What you resist persists. What you accept transforms."',
            '"Patience is not weakness. It is power held in reserve."',
        ],
        "art_style": "serene ink wash painting, Chinese shuimohua, Zen aesthetic, green/gold/ivory, morning light, negative space",
    },

    "Covenant Keepers": {
        "symbol": "⚖", "faith_color": "multi",
        "adjectives": ["united", "diplomatic", "interfaith", "bound", "sacred", "universal", "harmonious", "covenanted"],
        "servant_nouns": ["Diplomat", "Guardian", "Keeper", "Scholar", "Arbiter", "Ambassador", "Peacekeeper", "Warden"],
        "servant_types": ["Human / Diplomat", "Spirit / Arbiter", "Human / Scholar", "Multi-Faith / Guardian"],
        "proper_names": ["Sova", "Theodulus", "Miriam", "Quin Shao", "Kira", "Aliyah", "Benedikt", "Sakura"],
        "prayer_names": ["Sacred Accord", "Interfaith Treaty", "The Great Covenant", "Unity Prayer", "The Binding Word"],
        "miracle_names": ["Diplomatic Shield", "Sacred Intervention", "Unity Response", "Covenant Counter", "Arbiter's Will"],
        "covenant_names": ["The Grand Covenant", "Unity Pact", "Interfaith Accord", "Sacred Bond", "The Eternal Treaty"],
        "relic_names": ["Scales of Balance", "The Unity Seal", "Staff of Covenant", "Multi-Faith Talisman", "Diplomat's Sigil"],
        "shrine_names": ["Interfaith Temple", "The Sacred Meeting Hall", "Covenant Grounds", "Bridge of Faiths", "Unity Shrine"],
        "trap_names": ["Covenant Snare", "Diplomatic Trap", "Unity Counter", "Sacred Refusal", "The Arbiter's Judgment"],
        "keywords": ["Covenant", "Repent", "Vigilance", "Herald", "Undying Faith", "Pilgrimage", "Interfaith Bond"],
        "triggered_effects": [
            "When {NAME} enters: Search your deck for a Servant of any faction and add it to your hand.",
            "Whenever you play a Servant of a different faction: {NAME} gains a Unity counter (+200/+200 each).",
            "When {NAME} enters: All your Servants gain +200 ATK and +200 DEF until end of turn.",
            "Whenever you spend multi-faction Faith: Draw 1 card.",
            "At upkeep: If you control Servants of 3+ different factions, gain 500 Life Points.",
            "When {NAME} is destroyed: Return it to your hand at the start of your next turn.",
            "When {NAME} enters: Each player searches for a Shrine and puts it into play.",
        ],
        "activated_effects": [
            "{⚖}: Target Servant cannot be targeted by opponent's effects until your next turn.",
            "{2}{⚖}: All your Servants gain +500 ATK per different faction among them.",
            "{⚖}{⚖}: Copy target Prayer or Miracle. You may change its targets.",
        ],
        "prayer_effects": [
            "Search your deck for 1 Servant each of 3 different factions and add them to your hand.",
            "Until end of turn, your Servants gain +1000 ATK, or +2000 if you control 3+ faction Servants.",
            "Return all Servants from all Graveyards to the field under their original controllers.",
            "Exile all Covenants. Each player draws 3 cards.",
        ],
        "miracle_effects": [
            "Counter target spell. Search your deck for a Covenant and add it to your hand.",
            "Target Servant gains Diplomatic Immunity until your next turn.",
            "Copy target Prayer as it resolves. Choose new targets.",
            "Until end of turn, your Servants gain protection from all factions except yours.",
        ],
        "covenant_effects": [
            "You may use Faith of any color to pay colored costs of multi-faction cards.",
            "Whenever you play a multi-faction card, draw 1 card.",
            "All your Servants count as every faction for faction bonus purposes.",
            "Your opponent cannot use faction-hate effects against your Servants.",
        ],
        "relic_effects": [
            "Equipped Servant gains all keyword abilities of every faction represented among your Servants.",
            "Equipped Servant gains +500 ATK per different faction among your Servants.",
            "Once per turn: Move equipped Relic to any Servant. That Servant gains +400/+400.",
            "{⚖}: Equipped Servant gains any keyword of your choice until end of turn.",
        ],
        "shrine_effects": [
            "{Tap}: Add one Faith of any color to your Faith pool.",
            "{Tap}: Add {⚖}. If you control 3+ different faction Shrines, add {⚖}{⚖} instead.",
            "{Tap}: Add one Faith of any color. Once per turn, {1}: Add another Faith of any color.",
        ],
        "trap_effects": [
            "When your opponent targets a Servant you control: Counter that effect. Servant gains +500 ATK.",
            "When your opponent plays a Servant: Search your deck for a Servant of the same type and summon it.",
            "When your opponent activates any effect: Copy that effect, applying it to your side instead.",
        ],
        "flavor_quotes": [
            '"We do not choose between faiths. We carry them all."',
            '"Unity is not agreement. Unity is the decision to act together despite disagreement."',
            '"The bridge between our faiths is built from what we share, not from what divides us."',
            '"I have prayed in every language. The divine has answered in all of them."',
            '"A covenant made in good faith is stronger than any army."',
            '"When the faiths stand together, what force in the universe can oppose them?"',
            '"We do not ask which god you serve. We ask: are you willing to serve?"',
            '"Every sacred text agrees: treat others as you would be treated."',
        ],
        "art_style": "stained glass mosaic, Gothic cathedral glass, Islamic geometric art, rainbow/silver, prismatic light",
    },
}

# ────────────────────────────────────────────────────────────────────────────────
# DATA — RARITIES & CARD TYPES
# ────────────────────────────────────────────────────────────────────────────────

RARITIES = {
    "Common":    {"weight": 50, "max_cost": 3, "max_atk": 1600, "max_def": 1800, "abilities": 1, "star": 4, "badge": "◆ C"},
    "Uncommon":  {"weight": 30, "max_cost": 5, "max_atk": 2400, "max_def": 2600, "abilities": 2, "star": 5, "badge": "◇ U"},
    "Rare":      {"weight": 15, "max_cost": 7, "max_atk": 3000, "max_def": 3200, "abilities": 2, "star": 6, "badge": "◈ R"},
    "Legendary": {"weight": 5,  "max_cost": 9, "max_atk": 4000, "max_def": 4000, "abilities": 3, "star": 8, "badge": "◉ L"},
}

CARD_TYPES = ["Servant", "Prayer", "Miracle", "Covenant", "Relic", "Shrine", "Divine Trap"]

# ────────────────────────────────────────────────────────────────────────────────
# DATA — GAME CONCEPTS
# ────────────────────────────────────────────────────────────────────────────────

GAME_CONCEPTS = {
    "Faith Resource System": """
**Faith** is the core resource of Testament — analogous to Mana in Magic: The Gathering.

**Faith Symbols by Faction:**
- ✦ Celestial Host — White Faith (purity, protection, healing)
- ☽ Fallen Dominion — Black Faith (sacrifice, power, darkness)
- 📜 Prophetic Order — Blue Faith (knowledge, control, time)
- ⚡ Ancient Pantheon — Red Faith (raw power, chaos, destruction)
- ☸ Dharmic Path — Green Faith (nature, balance, growth)
- ⚖ Covenant Keepers — Multi-Faith (hybrid, versatile)

**Generating Faith:**
- Shrines produce 1 Faith per turn when tapped
- Players start with 3 Shrines in play; may play 1 Shrine per turn from hand
- Maximum 7 Shrines in play at once

**Faith Costs:**
- Generic Faith (any color): {1}, {2}, {3}...
- Colored Faith: {✦}, {☽}, {📜}, {⚡}, {☸}, {⚖}
- Example: {3}{✦}{✦} = 3 generic + 2 Celestial Faith
- Hybrid costs: {✦/☽} can be paid with either symbol
""",
    "Card Types": """
**SERVANT** (Creature equivalent)
Has ATK and DEF. Costs Faith to summon. Tribute rules: 5-6★ needs 1 Tribute; 7-8★ needs 2.

**PRAYER** (Sorcery equivalent)
Cast only during your Main Phase. Resolves immediately; goes to Graveyard after use.

**MIRACLE** (Instant equivalent)
Cast at ANY time, including opponent's turn and in response to other cards.

**COVENANT** (Enchantment equivalent)
Permanent card with an ongoing effect. Stays in play until destroyed.

**RELIC** (Artifact/Equipment)
Sacred objects, holy weapons. Some attach to Servants (+ATK/DEF). Some have activated abilities.

**SHRINE** (Land equivalent)
Generates 1 Faith of its color each turn when tapped. Free to play (1 per turn from hand).

**DIVINE TRAP** (Yugioh-style Trap)
Played face-down during your turn. Triggered by specific conditions on opponent's turn.
Set up to 3 Divine Traps face-down in your Trap Zone at a time.
""",
    "Turn Structure": """
**PHASE 1 — DAWN (Draw)**
Draw 1 card. If your deck is empty, you cannot draw (Judgment loss condition).

**PHASE 2 — FAITH (Resource)**
Untap all your tapped Shrines and Servants. Gain Faith from all untapped Shrines.
Faith pool resets each turn — unspent Faith does not carry over.

**PHASE 3 — MAIN (Action)**
Play Servants, Prayers, Covenants, Relics. Set Divine Traps face-down (free).
Place 1 Shrine from hand (free, once per turn). Activate abilities of permanents.

**PHASE 4 — BATTLE (Combat)**
Declare attackers (tap each). Opponent declares blockers.
Unblocked attackers deal ATK damage directly to opponent's Life Points.
Blocked combat: compare ATK vs DEF simultaneously.

**PHASE 5 — END (Cleanup)**
Discard down to 7 cards if over hand limit. Resolve end-of-turn effects.
Pass priority to opponent — their turn begins.
""",
    "Win Conditions": """
**1. DOMINION (Life Points)**
Reduce opponent's Life Points from 8000 to 0 through combat or card effects.

**2. JUDGMENT (Deck-Out)**
If a player must draw but their deck is empty, they lose immediately.
Prophetic Order specializes in this strategy.

**3. THE DIVINE RECKONING (Legendary Condition)**
Control all 5 of a faction's named Legendary Servants simultaneously.
Opponent has 1 full turn to disrupt after the 4th Legendary is played.
Only 1 copy of each Legendary allowed per deck.
""",
    "Tribute & Rarity": """
**TRIBUTE SYSTEM**
- ★★★★ or below: Normal Summon (no Tribute)
- ★★★★★–★★★★★★: Tribute Summon — sacrifice 1 Servant
- ★★★★★★★–★★★★★★★★: Tribute Summon — sacrifice 2 Servants
Only 1 Tribute Summon per turn.

**RARITY TIERS**
- ◆ Common (50%) — 1-3 Faith cost, ATK up to 1600, 1 ability
- ◇ Uncommon (30%) — 2-5 Faith cost, ATK up to 2400, 2 abilities
- ◈ Rare (15%) — 4-7 Faith cost, ATK up to 3000, 2 abilities
- ◉ Legendary (5%) — 6-9 Faith cost, ATK up to 4000, 3 abilities, max 1 copy per deck

**DECK BUILDING**
40–60 cards total. Max 3 copies of non-Legendary cards. Minimum 15 Shrines recommended.
""",
}

# ────────────────────────────────────────────────────────────────────────────────
# DATA — ABILITIES
# ────────────────────────────────────────────────────────────────────────────────

ABILITIES = [
    # Keywords
    {"name": "Consecrated", "cat": "Keyword", "rules": "Cannot be targeted by opponent's spells or abilities.", "faction": "Celestial Host", "power": 4},
    {"name": "Blessed", "cat": "Keyword", "rules": "Whenever this Servant deals combat damage, you gain that much Life Points.", "faction": "Celestial Host", "power": 3},
    {"name": "Herald", "cat": "Keyword", "rules": "When this enters: reveal top card of deck. If same faction Servant, put it in hand.", "faction": "Celestial Host", "power": 3},
    {"name": "Smite", "cat": "Keyword", "rules": "When this deals combat damage to a Servant, that Servant is destroyed at end of combat.", "faction": "Celestial Host / Pantheon", "power": 4},
    {"name": "Ascend", "cat": "Keyword", "rules": "Special Summon from Graveyard by paying {2} and revealing 3 faction cards in hand.", "faction": "Celestial Host", "power": 4},
    {"name": "Martyr", "cat": "Keyword", "rules": "When destroyed and sent to Graveyard: draw 1 card and gain 2 Life Points.", "faction": "Celestial Host / Prophetic", "power": 3},
    {"name": "Fallen", "cat": "Keyword", "rules": "Counts as both Celestial Host and Fallen Dominion for all game effects.", "faction": "Fallen Dominion", "power": 3},
    {"name": "Sanctify", "cat": "Keyword", "rules": "Once per turn: remove 1 Curse counter from a Servant you control. It gains +200 DEF.", "faction": "Celestial Host", "power": 2},
    {"name": "Divinity", "cat": "Keyword", "rules": "Cannot be destroyed by effects with a Faith cost of 3 or less.", "faction": "All (Legendary)", "power": 5},
    {"name": "Pilgrimage", "cat": "Keyword", "rules": "When this enters: search your deck for a Shrine and put it into play tapped.", "faction": "Dharmic / Covenant", "power": 4},
    {"name": "Exorcise", "cat": "Keyword", "rules": "Can block Fallen Dominion Servants for free. When it blocks a Demon, that Servant is banished.", "faction": "Celestial Host", "power": 4},
    {"name": "Repent", "cat": "Keyword", "rules": "At start of your turn, pay 2 Life Points to remove all negative counters from this.", "faction": "Covenant Keepers", "power": 2},
    {"name": "Wrath", "cat": "Keyword", "rules": "Gets +600 ATK while your Life Points are 3000 or less.", "faction": "Ancient Pantheon / Fallen", "power": 3},
    {"name": "Covenant", "cat": "Keyword", "rules": "This card's effects cannot be negated.", "faction": "Covenant Keepers", "power": 4},
    {"name": "Invoke", "cat": "Keyword", "rules": "Special Summon from hand by banishing 2 Servants of its faction from Graveyard.", "faction": "Fallen Dominion", "power": 4},
    {"name": "Radiant", "cat": "Keyword", "rules": "All Servants of your faction gain +200 ATK while this Servant is on the field.", "faction": "Celestial Host", "power": 4},
    {"name": "Transcend", "cat": "Keyword", "rules": "Cannot be targeted the turn it was summoned. +500 ATK if summoned from Graveyard.", "faction": "Dharmic / Pantheon", "power": 4},
    {"name": "Sacrifice", "cat": "Keyword", "rules": "When Tributed for a Tribute Summon, the summoned Servant enters with 2 extra +100 ATK counters.", "faction": "Fallen Dominion", "power": 3},
    {"name": "Undying Faith", "cat": "Keyword", "rules": "When this would be destroyed, return it to hand instead (once per turn).", "faction": "Celestial / Covenant", "power": 4},
    {"name": "Prophesy", "cat": "Keyword", "rules": "Once per turn: look at the top 2 cards of your deck. Put them back in any order.", "faction": "Prophetic Order", "power": 3},
    {"name": "Meditate", "cat": "Keyword", "rules": "Cannot attack. DEF equals ATK + 500 while in Defense Position.", "faction": "Dharmic Path", "power": 3},
    {"name": "Dharmic", "cat": "Keyword", "rules": "If this deals damage in excess of what destroys a Servant, distribute excess to another target.", "faction": "Dharmic Path", "power": 4},
    {"name": "Eternal", "cat": "Keyword", "rules": "Cannot be banished. When it would be banished, goes to Graveyard instead.", "faction": "All (Legendary)", "power": 4},
    {"name": "Corrupted", "cat": "Keyword", "rules": "Enters with 1 Corruption counter. Add 1 each turn. At 5 counters, this is destroyed.", "faction": "Fallen Dominion", "power": 2},
    {"name": "Divine Shield", "cat": "Keyword", "rules": "First time this would be destroyed each turn, prevent it and remove this keyword.", "faction": "Celestial Host", "power": 4},
    {"name": "Banish", "cat": "Keyword", "rules": "When this destroys a Servant in combat, banish that Servant instead of Graveyard.", "faction": "Celestial / Fallen", "power": 4},
    {"name": "Zealot", "cat": "Keyword", "rules": "Must attack each turn if able. Gains +500 ATK during the Battle Phase.", "faction": "Pantheon / Fallen", "power": 3},
    {"name": "Vigilance", "cat": "Keyword", "rules": "Does not tap when it attacks.", "faction": "Celestial / Covenant", "power": 3},
    {"name": "Flash", "cat": "Keyword", "rules": "May be summoned during opponent's turn or during your Battle Phase.", "faction": "Prophetic Order", "power": 4},
    {"name": "Soul Bind", "cat": "Keyword", "rules": "If this is destroyed, opponent must also destroy one of their Servants.", "faction": "Fallen Dominion", "power": 4},
    # Triggered
    {"name": "Heavenly Descent", "cat": "Triggered", "rules": "When ~ enters: Create two 1000/1000 Seraph tokens with Flying.", "faction": "Celestial Host", "power": 5},
    {"name": "Death Knell", "cat": "Triggered", "rules": "When ~ is destroyed: Deal 1000 damage to all opponents and each discards 1 card.", "faction": "Fallen Dominion", "power": 4},
    {"name": "Oracle's Vision", "cat": "Triggered", "rules": "Whenever you cast a Prayer: Draw 1 card. If it is a Prayer, cast it for free.", "faction": "Prophetic Order", "power": 5},
    {"name": "Thunder Strike", "cat": "Triggered", "rules": "Whenever ~ attacks: Deal 500 damage to target Servant or player.", "faction": "Ancient Pantheon", "power": 3},
    {"name": "Karmic Return", "cat": "Triggered", "rules": "Whenever opponent's effect would deal damage to you: Gain that much life instead.", "faction": "Dharmic Path", "power": 5},
    {"name": "Interfaith Bond", "cat": "Triggered", "rules": "Whenever you play a Servant of a different faction: +200/+200 Unity counter on ~.", "faction": "Covenant Keepers", "power": 4},
    {"name": "Resurrection Call", "cat": "Triggered", "rules": "When ~ is destroyed: Return target Servant ATK 1500 or less from Graveyard to battlefield.", "faction": "Celestial Host", "power": 4},
    {"name": "Demonic Possession", "cat": "Triggered", "rules": "When ~ enters: Take control of target opponent's Servant until ~ leaves play.", "faction": "Fallen Dominion", "power": 5},
    {"name": "Prophetic Warning", "cat": "Triggered", "rules": "At start of opponent's Combat Phase: Look at their hand. Choose 1 Servant — it cannot attack.", "faction": "Prophetic Order", "power": 4},
    {"name": "Cataclysm", "cat": "Triggered", "rules": "When ~ is destroyed: Destroy all Servants with ATK less than ~'s ATK.", "faction": "Ancient Pantheon", "power": 5},
    {"name": "Lotus Bloom", "cat": "Triggered", "rules": "At upkeep: Gain 1 life and add {☸}. If you have 10+ life, draw 1 card instead.", "faction": "Dharmic Path", "power": 3},
    {"name": "Sacred Covenant", "cat": "Triggered", "rules": "When ~ enters: Search deck for a Covenant card and put it into hand.", "faction": "Covenant Keepers", "power": 4},
    # Activated
    {"name": "Holy Judgment", "cat": "Activated", "rules": "{2}{✦}: Destroy target Servant with ATK 2000 or less. Main Phase only.", "faction": "Celestial Host", "power": 4},
    {"name": "Soul Harvest", "cat": "Activated", "rules": "{☽}: Sacrifice a Servant. Gain life equal to that Servant's ATK / 100.", "faction": "Fallen Dominion", "power": 3},
    {"name": "Arcane Study", "cat": "Activated", "rules": "{1}{📜}: Draw 2 cards, then discard 1. Main Phase only.", "faction": "Prophetic Order", "power": 4},
    {"name": "Divine Fury", "cat": "Activated", "rules": "{⚡}{⚡}: This Servant gains +1000 ATK until end of turn. Must attack if able.", "faction": "Ancient Pantheon", "power": 4},
    {"name": "Inner Peace", "cat": "Activated", "rules": "{☸}: Remove all negative effects and counters. Cannot be targeted until your next turn.", "faction": "Dharmic Path", "power": 4},
    {"name": "Interfaith Rally", "cat": "Activated", "rules": "{⚖}{⚖}: All Servants gain +500 ATK, or +1000 if you control 3+ different factions.", "faction": "Covenant Keepers", "power": 5},
    {"name": "Counter Spell", "cat": "Activated", "rules": "{1}{📜}: Counter target Prayer or Miracle. Activate when a Prayer or Miracle is cast.", "faction": "Prophetic Order", "power": 5},
    {"name": "Thunder God's Wrath", "cat": "Activated", "rules": "{⚡}{⚡}{⚡}: Deal 2000 damage to target Servant. 3000 if it has Consecrated.", "faction": "Ancient Pantheon", "power": 5},
    {"name": "Zen Focus", "cat": "Activated", "rules": "{1}{☸}: Damage you would take is reduced by 500 until end of turn (minimum 0).", "faction": "Dharmic Path", "power": 3},
    {"name": "Diplomatic Immunity", "cat": "Activated", "rules": "{⚖}: Target Servant cannot be targeted until your next turn. Activate on opponent's turn.", "faction": "Covenant Keepers", "power": 4},
    # Static
    {"name": "Celestial Aura", "cat": "Static", "rules": "All Celestial Host Servants you control get +300 ATK and +300 DEF.", "faction": "Celestial Host", "power": 4},
    {"name": "Lord of Darkness", "cat": "Static", "rules": "All Fallen Dominion Servants get +500 ATK. Each opponent's Servant loses 200 ATK.", "faction": "Fallen Dominion", "power": 5},
    {"name": "Forbidden Knowledge", "cat": "Static", "rules": "Prayers and Miracles you cast cost {1} less (minimum {1}).", "faction": "Prophetic Order", "power": 4},
    {"name": "Olympian Presence", "cat": "Static", "rules": "Opponent's Servants lose 200 ATK for each God-type Servant you control.", "faction": "Ancient Pantheon", "power": 4},
    {"name": "Enlightened Path", "cat": "Static", "rules": "At start of your turn, if you have more life than opponent, draw an extra card.", "faction": "Dharmic Path", "power": 4},
    {"name": "Bridge of Faith", "cat": "Static", "rules": "You may use Faith of any color to pay the colored costs of multi-faction cards.", "faction": "Covenant Keepers", "power": 5},
    {"name": "Holy Ground", "cat": "Static", "rules": "Fallen Dominion Servants lose 500 ATK while on this field. Cannot be negated.", "faction": "Celestial Host", "power": 4},
    {"name": "Seeker of Truth", "cat": "Static", "rules": "Your hand size maximum is 10 instead of 7.", "faction": "Prophetic Order", "power": 4},
    {"name": "Karmic Balance", "cat": "Static", "rules": "If your life is less than opponent's, Servants get +200 ATK. If greater, +200 DEF.", "faction": "Dharmic Path", "power": 3},
    {"name": "Pantheon Lord", "cat": "Static", "rules": "Whenever a Servant you control deals damage, that damage is increased by 200.", "faction": "Ancient Pantheon", "power": 4},
]

# ────────────────────────────────────────────────────────────────────────────────
# DATA — FACTION GUIDE SUMMARIES
# ────────────────────────────────────────────────────────────────────────────────

FACTION_GUIDE = {
    "Celestial Host ✦": {
        "lore": "The Celestial Host are the armies of Heaven — angels, archangels, seraphim, and mortal saints elevated to divine service. Organized under a hierarchy of perfect order, they exist to protect the sacred, heal the wounded, and purge corruption. Their Faith is blazing divine light that reveals and burns away all that is false. They do not hate their enemies; they execute judgment with love, believing that even destruction can be an act of mercy.",
        "figures": [("Archangel Michael", "Commander of Heaven's armies; Sword of Truth; anti-Demon specialist"), ("Archangel Gabriel", "The Herald; divine messenger; strongest Prayer/Miracle synergy"), ("Archangel Raphael", "The Healer; life restoration master; key to healing-win strategies"), ("Archangel Uriel", "The Flame of God; guardian; exile specialist"), ("Seraph Luminara", "Six-winged; creates Seraph tokens; swarm enabler"), ("Guardian Tael", "Heaven's gatekeeper; prevents combat damage to allies")],
        "playstyle": "Protective and resource-efficient. Excels at maintaining board presence and grinding opponents down. Protects key Servants with Consecrated and Divine Shield, heals back damage, and uses exile effects to permanently remove threats.",
        "strengths": ["Outstanding defensive capabilities", "Strong anti-Fallen Dominion exile effects", "Excellent card advantage through Herald chains", "Life gain prevents Dominion loss condition", "Consecrated blocks many removal spells"],
        "weaknesses": ["Relatively low ATK — relies on evasion over raw power", "Weak against Ancient Pantheon's non-targeted board wipes", "Expensive top-end requires careful Shrine building"],
        "counter": "Attack the mana base — destroy Shrines early. Use mass effects that hit all Servants simultaneously (they bypass Consecrated). Fill their Graveyard then banish it to cut off Ascend recursion.",
    },
    "Fallen Dominion ☽": {
        "lore": "Once among Heaven's most radiant servants, the Fallen chose pride over obedience and were cast into the abyss — not broken, but transformed. The Fallen Dominion is a realm of terrible beauty and absolute power, where strength is earned through sacrifice. They believe true power requires the willingness to consume all — even oneself — in its pursuit.",
        "figures": [("Archfiend Malphas", "Fallen general; master of corruption; steals opponent's Servants"), ("Sin Incarnate Avaric", "Embodies Greed; generates massive Faith from sacrifices"), ("Demon Prince Vasrath", "Destruction specialist; high ATK glass cannon"), ("Fallen Seraph Marev", "Former angel; retains angelic beauty with demonic power; dual-faction"), ("Shadow Apostle Kael", "Corrupted prophet; hand disruption specialist")],
        "playstyle": "High-risk, high-reward aggression and sacrifice. Sacrifices weaker Servants to fuel more powerful ones, drains opponent's resources through hand disruption and life damage, and establishes overwhelming board states through sheer destructive force.",
        "strengths": ["Highest raw ATK values", "Graveyard recursion makes threats hard to permanently remove", "Hand disruption cripples control strategies", "Sacrifice mechanics generate resource advantages"],
        "weaknesses": ["Low DEF — vulnerable to being outpaced", "Self-destructive Corrupted mechanics can backfire", "Heavily countered by Celestial Host exile effects"],
        "counter": "Banish everything — don't let cards go to the Graveyard. Heal aggressively to weather early bursts. Force them to sacrifice too early; they will run out of fuel.",
    },
    "Prophetic Order 📜": {
        "lore": "The Prophetic Order are keepers of divine revelation — prophets, apostles, scribes, sages, and oracles who have been granted visions of what was, what is, and what will be. They do not fight with brute force; they fight with information, timing, and the art of ensuring that every move their opponent makes leads to ruin.",
        "figures": [("The Prophet Eliyah", "Sees 5 turns ahead; Prophesy passive; perfect sequence setup"), ("Apostle Petrus", "Resilient blocker with hand-refill abilities; defensive cornerstone"), ("Oracle Delphis", "Legendary foreseer; ultimate control lock"), ("Sage Morrigan", "Every 5 cards drawn triggers a free Miracle"), ("Apostle Malkiel", "Has built-in Counter Spell on his body")],
        "playstyle": "Plays the long game. Draws cards constantly, counters key plays, and slowly builds insurmountable advantage. Aims for Judgment (deck-out) while protecting itself with Flash Servants and instant-speed Miracles.",
        "strengths": ["Unmatched card advantage", "Counterspells negate the most powerful effects", "Judgment win condition is completely different to play around", "Flash Servants are unpredictable"],
        "weaknesses": ["Low ATK — vulnerable to pure aggression", "Judgment strategy fails if opponent has library protection", "Weak against Fallen Dominion's hand disruption"],
        "counter": "Relentless aggression. Force them to spend counterspells on creatures. Cards that say 'this cannot be countered' are hard counters. Speed — win before turn 6.",
    },
    "Ancient Pantheon ⚡": {
        "lore": "Before the current age, other gods held sway — the Greek Olympians, Norse Aesir, Egyptian Ennead, Aztec Teteo. The Ancient Pantheon is not united — it is a gathering of ancient powers who share only their immense, barely-contained strength. They do not plan. They do not need to. They simply are — and their existence alone reshapes the world.",
        "figures": [("Zeus Pantokrator", "King of Olympians; direct damage to any target every turn"), ("Odin Allfather", "Wisdom and war; Prophesy on a body with war-god ATK"), ("Ra, Eye of Heaven", "Egyptian sun god; heals equal to damage dealt each turn"), ("Quetzalcoatl", "Feathered Serpent; mass destruction on summon"), ("Kali the Destroyer", "Board wipe as an activated ability"), ("Thor Thunderborn", "Attacks twice per Battle Phase")],
        "playstyle": "Pure power faction. Servants have the highest combined ATK. Overwhelm with sheer force, punish blockers with Cataclysm triggers, use non-targeted effects to bypass Consecrated.",
        "strengths": ["Highest ATK stats", "Non-targeted effects bypass most protection", "Devastating board wipes at large Servant count", "Wrath ability turns near-defeat into power spike"],
        "weaknesses": ["Expensive costs require many Red Shrines", "Low DEF — vulnerable before setup", "Forced attacks (Zealot) can be exploited", "Limited card draw"],
        "counter": "A Consecrated blocker in Defense Position can stall while you build. Force sacrifice effects remove their best attacker cheaply. Prophetic Order counters their most expensive Gods before they land.",
    },
    "Dharmic Path ☸": {
        "lore": "The Dharmic Path encompasses Eastern spiritual traditions — Buddhist monks seeking enlightenment, Hindu Devas maintaining cosmic order, Taoist masters embodying nature's flow. Their Faith is green — of growing things, of rivers that carve stone through patience. They believe victory is achieved not by defeating enemies but by achieving such profound harmony that no enemy can gain a foothold.",
        "figures": [("Bodhisattva Avalokita", "Compassion manifest; heals all allies every turn"), ("Lord Brahma the Creator", "Creates two Spirit tokens each turn; endless resources"), ("Sage Sun Wukong", "Trickster monk; steals abilities temporarily"), ("Dragon King Ryujin", "Massive DEF; cannot be destroyed by combat"), ("Enlightened One Siddhi", "Reaching 10 Karma counters triggers alternate win"), ("Durga Mahashakti", "Nine-armed warrior; fights eight Servants simultaneously")],
        "playstyle": "Turns opponent's strengths against them. Maintains high DEF to survive aggression, accumulates life through Karma mechanics, and uses Karmic Return to convert damage into healing. Prefers long games.",
        "strengths": ["Highest DEF values — hard to overcome in combat", "Karmic Return makes damage strategies backfire", "Sustainable resource generation", "Strong in long games"],
        "weaknesses": ["Low ATK — cannot pressure opponent proactively", "Pantheon's non-targeted effects bypass Karmic Return", "Susceptible to Judgment strategies"],
        "counter": "Non-targeted mass damage. Ancient Pantheon's area effects cannot be Karmic-Returned. Direct Judgment ignores their life total. Effects preventing healing cut off their engine.",
    },
    "Covenant Keepers ⚖": {
        "lore": "There are those who refuse the easy certainty of a single faith. The Covenant Keepers are diplomats, syncretics, scholars of comparative theology, and warriors who have sworn oaths to protect all sacred traditions equally. Their symbol is the scales — not because they are neutral, but because they understand that balance between all forces creates something greater than any one force could alone.",
        "figures": [("The Arbiter of Faiths", "Legendary; can use abilities of ANY faction's Servants"), ("Interfaith Guardian Sova", "Gains abilities from each nearby faction's Servant"), ("Scholar Theodulus", "Knows every ability as an activated ability"), ("Diplomat Quin Shao", "Diplomatic Immunity aura; protects all your Servants"), ("Unity Seeker Kira", "Builds Unity counters faster than any other card")],
        "playstyle": "The combo and synergy faction. Combines mechanics from multiple factions — sacrifice to fuel healing, card draw to find finishers. Bridge of Faith makes multi-faction costs trivial. Unity counters reward diversity.",
        "strengths": ["Accesses mechanics from all factions — extreme versatility", "Unity counter scaling makes late-game boards overwhelming", "Bridge of Faith makes deck construction flexible", "Best matchup spread — no hard faction counters"],
        "weaknesses": ["No native faction hate effects", "Consistency can be an issue with diverse card pool", "Medium stats — not best at anything specifically"],
        "counter": "Target the Shrines. Covenant Keepers need multiple Faith types — disrupting their Shrine setup prevents multi-faction casting. Counter key Covenant cards before they hit the field.",
    },
}

# ────────────────────────────────────────────────────────────────────────────────
# DATA — ART STYLES
# ────────────────────────────────────────────────────────────────────────────────

ART_STYLES = {
    "Celestial Host": {"style": "baroque religious painting", "palette": "gold, white, ivory, soft blue", "lighting": "divine backlighting, volumetric light rays", "influences": "Raphael, Michelangelo, Byzantine iconography", "neg": "dark, gloomy, demonic, low quality"},
    "Fallen Dominion": {"style": "gothic dark fantasy", "palette": "deep crimson, obsidian black, sickly purple", "lighting": "hellfire glow, bioluminescent corruption", "influences": "John Martin, Gustave Doré, Ars Goetia", "neg": "bright, cheerful, cartoonish, low quality"},
    "Prophetic Order": {"style": "illuminated manuscript", "palette": "deep blue, earth brown, gold leaf, parchment", "lighting": "candlelight, moonlight through windows", "influences": "Book of Kells, Persian miniature, Quran calligraphy", "neg": "modern, bright neon, low quality"},
    "Ancient Pantheon": {"style": "epic mythology painting", "palette": "bold red, burning orange, electric gold, bronze", "lighting": "dramatic chiaroscuro, lightning, fire, sun rays", "influences": "Jacques-Louis David, Greek vase painting, Egyptian relief", "neg": "subtle, quiet, modern, low quality"},
    "Dharmic Path": {"style": "serene ink wash painting", "palette": "sage green, lotus gold, ivory, muted jade", "lighting": "soft diffuse light, morning sunlight", "influences": "Chinese shuimohua, Japanese Zen, Tibetan thangka", "neg": "violent, dark, chaotic, low quality"},
    "Covenant Keepers": {"style": "stained glass mosaic", "palette": "rainbow prismatic, silver, warm gold, crystal blue", "lighting": "light through stained glass, prismatic rainbows", "influences": "Gothic cathedral glass, Islamic geometric art", "neg": "monochrome, divisive, dark, low quality"},
}

COMP_TEMPLATES = {
    "Servant": "full figure or bust portrait, heroic pose, low-angle perspective, subject as focal point",
    "Prayer": "wide shot of ritual in progress, radiating light patterns, divine intervention scene",
    "Miracle": "dramatic split-second action shot, explosive energy, reality cracking open",
    "Covenant": "formal symmetrical composition, ceremonial framing, sacred geometry, timeless",
    "Relic": "object-focused still life, dramatic lighting on the item, reverent framing, pedestal or altar",
    "Shrine": "wide establishing shot of architectural structure in its environment, sense of scale",
    "Divine Trap": "hidden/reveal tension composition, dramatic shadow, trap seal visible, anticipation",
}

# ────────────────────────────────────────────────────────────────────────────────
# GENERATION LOGIC
# ────────────────────────────────────────────────────────────────────────────────

def pick_rarity():
    weights = [RARITIES[r]["weight"] for r in RARITIES]
    return random.choices(list(RARITIES.keys()), weights=weights, k=1)[0]


def build_faith_cost(faction_data, rarity_data):
    symbol = faction_data["symbol"]
    max_cost = rarity_data["max_cost"]
    total = random.randint(max(1, max_cost - 2), max_cost)
    colored = random.randint(1, min(2 if faction_data["faith_color"] == "multi" else 3, total))
    generic = total - colored
    cost_str = (f"{{{generic}}}" if generic > 0 else "") + f"{{{symbol}}}" * colored
    return cost_str, total


def count_cost(cost_str):
    total = 0
    for m in re.findall(r'\{([^}]+)\}', cost_str):
        total += int(m) if m.isdigit() else 1
    return total


def build_servant_name(faction_data, rarity, concept):
    cl = concept.lower()
    for pname in faction_data["proper_names"]:
        if pname.lower() in cl:
            return f"{random.choice(faction_data['servant_nouns'])} {pname}", random.choice(faction_data["servant_types"])
    if rarity in ("Rare", "Legendary") and random.random() > 0.4:
        return f"{random.choice(faction_data['servant_nouns'])} {random.choice(faction_data['proper_names'])}", random.choice(faction_data["servant_types"])
    return f"{random.choice(faction_data['adjectives']).title()} {random.choice(faction_data['servant_nouns'])}", random.choice(faction_data["servant_types"])


def build_card_name(faction_data, card_type, concept):
    pools = {
        "Prayer": faction_data["prayer_names"], "Miracle": faction_data["miracle_names"],
        "Covenant": faction_data["covenant_names"], "Relic": faction_data["relic_names"],
        "Shrine": faction_data["shrine_names"], "Divine Trap": faction_data["trap_names"],
    }
    pool = pools.get(card_type, faction_data["prayer_names"])
    cl = concept.lower()
    for name in pool:
        for word in cl.split():
            if len(word) > 3 and word in name.lower():
                return name
    return random.choice(pool)


def build_atk_def(rarity_data, cost_total):
    max_atk, max_def = rarity_data["max_atk"], rarity_data["max_def"]
    scale = max(0.5, min(1.0, cost_total / rarity_data["max_cost"]))
    atk = int(random.randint(int(max_atk * 0.6), max_atk) * scale / 100) * 100
    def_ = int(random.randint(int(max_def * 0.5), max_def) * scale / 100) * 100
    return atk, def_


def build_abilities(faction_data, card_type, rarity, name):
    num = RARITIES[rarity]["abilities"]
    result = [random.choice(faction_data["keywords"])]
    if num >= 2:
        if card_type == "Servant":
            pool = faction_data["triggered_effects"] + faction_data["activated_effects"]
        elif card_type == "Prayer":     pool = faction_data["prayer_effects"]
        elif card_type == "Miracle":    pool = faction_data["miracle_effects"]
        elif card_type == "Covenant":   pool = faction_data["covenant_effects"]
        elif card_type == "Relic":      pool = faction_data["relic_effects"]
        elif card_type == "Shrine":     pool = faction_data["shrine_effects"]
        elif card_type == "Divine Trap": pool = faction_data["trap_effects"]
        else:                           pool = faction_data["triggered_effects"]
        result.append(random.choice(pool).replace("{NAME}", name))
    if num >= 3:
        extras = [e for e in faction_data.get("triggered_effects", []) + faction_data.get("activated_effects", []) if e not in result]
        if extras:
            result.append(random.choice(extras).replace("{NAME}", name))
    return result


def generate_card(faction_name, card_type, concept):
    fd = FACTIONS[faction_name]
    rarity = pick_rarity()
    rd = RARITIES[rarity]
    cost_str, cost_total = build_faith_cost(fd, rd)

    if card_type == "Servant":
        name, subtype = build_servant_name(fd, rarity, concept)
        type_line = f"Servant — {subtype} [{faction_name}]"
    else:
        name = build_card_name(fd, card_type, concept)
        type_line = f"{card_type} [{faction_name}]"

    atk, def_ = build_atk_def(rd, cost_total) if card_type == "Servant" else (None, None)
    abilities = build_abilities(fd, card_type, rarity, name)
    flavor = random.choice(fd["flavor_quotes"])
    art_desc = f"{concept}, " + fd["art_style"] if concept else name.lower() + ", " + fd["art_style"]

    return {
        "name": name, "cost": cost_str, "rarity": rarity, "badge": rd["badge"],
        "type_line": type_line, "card_type": card_type,
        "atk": atk, "def": def_, "stars": rd["star"],
        "abilities": abilities, "flavor": flavor, "art_desc": art_desc,
        "faction": faction_name, "symbol": fd["symbol"],
    }


def build_art_prompts(card):
    art = card["art_desc"]
    fname = card["faction"]
    style = ART_STYLES.get(fname, {})
    comp = COMP_TEMPLATES.get(card["card_type"], "portrait composition")

    mj = (f"/imagine prompt: {art}, TCG card illustration, {style.get('style','')}, "
          f"{comp}, {style.get('lighting','')}, {style.get('palette','')}, "
          f"highly detailed, masterpiece --ar 3:4 --v 6 --stylize 750 --quality 2")

    dalle = (f"Create a professional trading card game illustration of {art}. "
             f"Art style: {style.get('style','')} influenced by {style.get('influences','')}. "
             f"Composition: {comp}. Lighting: {style.get('lighting','')}. "
             f"Color palette: {style.get('palette','')}. "
             f"High detail, premium TCG card art quality.")

    sd_pos = (f"{art}, TCG illustration, {style.get('style','')}, {comp}, "
              f"{style.get('lighting','')}, {style.get('palette','')}, "
              f"highly detailed, masterpiece, best quality, 8k, professional concept art")
    sd_neg = (f"{style.get('neg', '')}, deformed, ugly, blurry, low quality, "
              f"watermark, text, NSFW, oversaturated, pixelated")

    return {"midjourney": mj, "dalle": dalle, "sd_pos": sd_pos, "sd_neg": sd_neg}


# ────────────────────────────────────────────────────────────────────────────────
# CARD ASCII RENDERER (plain text, no Rich markup)
# ────────────────────────────────────────────────────────────────────────────────

def render_card_ascii(card):
    W = 49  # inner content width; total card width = W + 4 (║ + space each side)
    sym = card["symbol"]
    badge = card["badge"]

    def wrap(text, width):
        words = text.split()
        lines, cur = [], ""
        for w in words:
            if len(cur) + len(w) + (1 if cur else 0) <= width:
                cur += (" " if cur else "") + w
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines or [""]

    border = "═" * (W + 2)
    sep    = f"╠{border}╣"

    # ── Title row ────────────────────────────────────────────────────────────────
    name_u  = card["name"].upper()
    cost    = card["cost"]
    name_w  = W + 2 - len(cost) - 1
    name_d  = name_u[:name_w].ljust(name_w)
    title_row = f"║ {name_d}{cost} ║"

    # ── Art rows ─────────────────────────────────────────────────────────────────
    art_w = W - 8  # [ART: ] = 6 chars + ] = 1 char + 1 space margin
    art_desc_clean = card["art_desc"].split(",")[0].strip()
    art_lines = wrap(art_desc_clean, art_w)
    art_row1 = f"║  [ART: {art_lines[0]:<{art_w}}]  ║"
    art_row2 = f"║         {art_lines[1]:<{art_w - 2}}   ║" if len(art_lines) > 1 else f"║{' ' * (W + 2)}║"

    # ── Type line ─────────────────────────────────────────────────────────────────
    type_row = f"║ {card['type_line']:<{W + 1}}║"

    # ── Abilities ─────────────────────────────────────────────────────────────────
    keyword = card["abilities"][0] if card["abilities"] else ""
    kw_row  = f"║ {keyword:<{W + 1}}║"
    blank   = f"║{' ' * (W + 2)}║"

    extra_rows = []
    for ab in card["abilities"][1:]:
        for line in wrap(ab, W):
            extra_rows.append(f"║ {line:<{W + 1}}║")
        extra_rows.append(blank)

    # ── Flavor text ────────────────────────────────────────────────────────────────
    flavor_clean = card["flavor"].strip('"').strip("'")
    flavor_lines = wrap(f'"{flavor_clean}"', W)
    flavor_rows = [f"║ {fl:<{W + 1}}║" for fl in flavor_lines]

    # ── ATK/DEF row ─────────────────────────────────────────────────────────────
    if card["atk"] is not None:
        stat_l = f"ATK: {card['atk']}   DEF: {card['def']}"
        stat_r = f"{sym * 3}  {badge}"
        pad    = W + 2 - len(stat_l) - len(stat_r)
        stat_row = f"║ {stat_l}{' ' * max(0, pad)}{stat_r} ║"
    else:
        stat_row = f"║{' ' * (W - len(badge) - 2)}{badge}   {sym} ║"

    # ── Assemble ──────────────────────────────────────────────────────────────────
    lines = [
        f"╔{border}╗",
        title_row,
        sep,
        art_row1,
        art_row2,
        sep,
        type_row,
        sep,
        kw_row,
        blank,
    ]
    lines.extend(extra_rows)
    lines.extend(flavor_rows)
    lines.append(blank)
    lines.append(sep)
    lines.append(stat_row)
    lines.append(f"╚{border}╝")

    return "\n".join(lines)


def build_save_text(card, prompts):
    lines = [
        "=== TESTAMENT TCG — Generated Card ===",
        f"Name:    {card['name']}",
        f"Faction: {card['faction']}",
        f"Type:    {card['type_line']}",
        f"Cost:    {card['cost']}",
        f"Rarity:  {card['rarity']}",
    ]
    if card["atk"] is not None:
        lines.append(f"ATK: {card['atk']}  /  DEF: {card['def']}")
    lines += ["", "Abilities:"] + [f"  • {a}" for a in card["abilities"]]
    lines += ["", f"Flavor: {card['flavor']}", "", f"Art:    {card['art_desc']}", ""]
    lines += [
        "--- ART PROMPTS ---", "",
        "MIDJOURNEY:", prompts["midjourney"], "",
        "DALL-E 3:", prompts["dalle"], "",
        "STABLE DIFFUSION (Positive):", prompts["sd_pos"], "",
        "STABLE DIFFUSION (Negative):", prompts["sd_neg"], "",
        "=== Generated by Testament TCG Engine ===",
    ]
    return "\n".join(lines)


# ────────────────────────────────────────────────────────────────────────────────
# STREAMLIT UI
# ────────────────────────────────────────────────────────────────────────────────

def css():
    st.markdown("""
    <style>
    .card-box { font-family: monospace; font-size: 13px; background: #1a1a2e;
                border: 1px solid #ffd700; border-radius: 6px; padding: 16px;
                color: #e8e8e8; white-space: pre; overflow-x: auto; }
    .prompt-box { font-family: monospace; font-size: 12px; background: #0e1117;
                  border: 1px solid #444; border-radius: 4px; padding: 12px;
                  color: #ccc; white-space: pre-wrap; word-break: break-word; }
    .faction-badge { display:inline-block; padding:4px 12px; border-radius:12px;
                     background:#1a1a2e; border:1px solid #ffd700; color:#ffd700;
                     font-size:14px; margin-bottom:8px; }
    h1, h2, h3 { color: #ffd700 !important; }
    .stSelectbox label, .stTextInput label, .stRadio label { color: #ffd700 !important; }
    </style>
    """, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────────
# GENERATOR HELPERS — session state & per-field regeneration
# ────────────────────────────────────────────────────────────────────────────────

def _load_card_to_state(card: dict):
    """Write a freshly generated card into all edit_* session-state keys."""
    abilities = card.get("abilities", [])
    st.session_state.update({
        "ws_faction":    card["faction"],
        "ws_card_type":  card["card_type"],
        "edit_name":     card["name"],
        "edit_cost":     card["cost"],
        "edit_rarity":   card["rarity"],
        "edit_type_line": card["type_line"],
        "edit_ab0":      abilities[0] if len(abilities) > 0 else "",
        "edit_ab1":      abilities[1] if len(abilities) > 1 else "",
        "edit_ab2":      abilities[2] if len(abilities) > 2 else "",
        "edit_flavor":   card["flavor"],
        "edit_atk":      int(card["atk"]) if card["atk"] is not None else 0,
        "edit_def":      int(card["def"]) if card["def"] is not None else 0,
        "edit_art_desc": card["art_desc"],
        "card_generated": True,
    })


def _card_from_state() -> dict:
    """Build a card dict from the current edit_* session-state values."""
    faction   = st.session_state.get("ws_faction",   "Celestial Host")
    card_type = st.session_state.get("ws_card_type", "Servant")
    rarity    = st.session_state.get("edit_rarity",  "Common")
    abilities = [a for a in [
        st.session_state.get("edit_ab0", ""),
        st.session_state.get("edit_ab1", ""),
        st.session_state.get("edit_ab2", ""),
    ] if a.strip()]
    is_servant = (card_type == "Servant")
    return {
        "name":      st.session_state.get("edit_name", ""),
        "cost":      st.session_state.get("edit_cost", ""),
        "rarity":    rarity,
        "badge":     RARITIES[rarity]["badge"],
        "type_line": st.session_state.get("edit_type_line", ""),
        "card_type": card_type,
        "atk":       int(st.session_state.get("edit_atk", 0)) if is_servant else None,
        "def":       int(st.session_state.get("edit_def", 0)) if is_servant else None,
        "stars":     RARITIES[rarity]["star"],
        "abilities": abilities if abilities else ["—"],
        "flavor":    st.session_state.get("edit_flavor", ""),
        "art_desc":  st.session_state.get("edit_art_desc", ""),
        "faction":   faction,
        "symbol":    FACTIONS[faction]["symbol"],
    }


def _regen_effect(faction_name: str, card_type: str, card_name: str) -> str:
    """Pick a random triggered/activated/spell effect for the given type."""
    fd = FACTIONS[faction_name]
    pools = {
        "Servant":    fd["triggered_effects"] + fd["activated_effects"],
        "Prayer":     fd["prayer_effects"],
        "Miracle":    fd["miracle_effects"],
        "Covenant":   fd["covenant_effects"],
        "Relic":      fd["relic_effects"],
        "Shrine":     fd["shrine_effects"],
        "Divine Trap": fd["trap_effects"],
    }
    pool = pools.get(card_type, fd["triggered_effects"])
    return random.choice(pool).replace("{NAME}", card_name)


# ────────────────────────────────────────────────────────────────────────────────
# GENERATOR PAGE — forge + workshop
# ────────────────────────────────────────────────────────────────────────────────

def _regen_btn(label: str, key: str, help_text: str = "") -> bool:
    """Compact 🔄 button that sits beside a field."""
    st.markdown("<div style='margin-top:22px'></div>", unsafe_allow_html=True)
    return st.button(label, key=key, help=help_text, use_container_width=True)


def page_generator():
    st.header("🃏 Card Generator")

    # ── Top bar: faction / type / concept / name ──────────────────────────────
    c1, c2, c3, c4 = st.columns([2, 2, 3, 2])
    with c1:
        faction_sel = st.selectbox("Faction", list(FACTIONS.keys()) + ["★ Surprise Me"], key="sel_faction")
    with c2:
        type_sel = st.selectbox("Card Type", CARD_TYPES + ["★ Surprise Me"], key="sel_type")
    with c3:
        concept = st.text_input("Concept / Idea", placeholder="e.g. angel who guards heaven", key="sel_concept")
    with c4:
        name_override = st.text_input("Card Name (optional)", placeholder="Leave blank to auto-generate", key="sel_name_override")

    sc1, sc2, sc3 = st.columns([2, 2, 1])
    with sc1:
        use_seed = st.checkbox("Lock seed (reproducible)", value=False, key="use_seed")
    with sc2:
        if st.session_state.get("use_seed"):
            st.number_input("Seed", 0, 99999, 42, key="seed_val")
    with sc3:
        generate = st.button("⚡ FORGE CARD", type="primary", use_container_width=True)

    # ── Handle initial generation ─────────────────────────────────────────────
    if generate:
        if st.session_state.get("use_seed"):
            random.seed(int(st.session_state.get("seed_val", 42)))
        else:
            random.seed()
        faction_name = random.choice(list(FACTIONS.keys())) if faction_sel == "★ Surprise Me" else faction_sel
        card_type    = random.choice(CARD_TYPES)             if type_sel   == "★ Surprise Me" else type_sel
        card = generate_card(faction_name, card_type, concept.strip())
        if name_override.strip():
            card["name"] = name_override.strip()
        _load_card_to_state(card)
        st.rerun()

    if not st.session_state.get("card_generated"):
        st.info("Choose options above and click ⚡ FORGE CARD to generate your first card.")
        return

    st.divider()
    faction   = st.session_state.get("ws_faction",   "Celestial Host")
    card_type = st.session_state.get("ws_card_type", "Servant")

    # ── Two-column workshop ───────────────────────────────────────────────────
    col_preview, col_editor = st.columns([1, 1], gap="large")

    # ── LEFT: Live card preview ───────────────────────────────────────────────
    with col_preview:
        card = _card_from_state()
        st.markdown(f'<div class="card-box">{render_card_ascii(card)}</div>', unsafe_allow_html=True)
        st.caption(f"**{card['rarity']}** · {card['faction']} · {card['card_type']}")
        prompts   = build_art_prompts(card)
        save_text = build_save_text(card, prompts)
        filename  = f"{card['name'].replace(' ', '_')}_{card['rarity']}.txt"
        st.download_button("💾 Download Card + Art Prompts (.txt)",
                           data=save_text, file_name=filename,
                           mime="text/plain", use_container_width=True)

    # ── RIGHT: Field editor ───────────────────────────────────────────────────
    with col_editor:
        st.subheader("Edit Fields")
        st.caption("Type directly or click 🔄 to regenerate any piece individually.")

        # — Name —
        nc, nb = st.columns([5, 1])
        with nc: st.text_input("Card Name", key="edit_name")
        with nb:
            if _regen_btn("🔄", "rn", "Regenerate name"):
                fd = FACTIONS[faction]
                if card_type == "Servant":
                    new_name, _ = build_servant_name(fd, st.session_state.get("edit_rarity", "Common"), concept)
                else:
                    new_name = build_card_name(fd, card_type, st.session_state.get("sel_concept", ""))
                st.session_state["edit_name"] = new_name
                st.rerun()

        # — Faith Cost + Rarity —
        costc, costr, rarc, rarb = st.columns([3, 1, 3, 1])
        with costc: st.text_input("Faith Cost", key="edit_cost", help="e.g. {2}{✦}{✦}")
        with costr:
            if _regen_btn("🔄", "rc", "Regenerate cost"):
                new_cost, _ = build_faith_cost(FACTIONS[faction], RARITIES[st.session_state.get("edit_rarity", "Common")])
                st.session_state["edit_cost"] = new_cost
                st.rerun()
        with rarc: st.selectbox("Rarity", list(RARITIES.keys()), key="edit_rarity")
        with rarb:
            if _regen_btn("🔄", "rrar", "Randomize rarity"):
                st.session_state["edit_rarity"] = pick_rarity()
                st.rerun()

        # — Type Line —
        st.text_input("Type Line", key="edit_type_line",
                      help="e.g. Servant — Angel / Archangel [Celestial Host]")

        st.markdown("---")
        st.markdown("**Abilities**")

        # — Keyword (slot 0) —
        ab0c, ab0b = st.columns([5, 1])
        with ab0c: st.text_input("① Keyword", key="edit_ab0")
        with ab0b:
            if _regen_btn("🔄", "rab0", "Regenerate keyword"):
                st.session_state["edit_ab0"] = random.choice(FACTIONS[faction]["keywords"])
                st.rerun()

        # — Ability 2 (slot 1) —
        ab1c, ab1b = st.columns([5, 1])
        with ab1c: st.text_area("② Effect", key="edit_ab1", height=90)
        with ab1b:
            if _regen_btn("🔄", "rab1", "Regenerate effect"):
                st.session_state["edit_ab1"] = _regen_effect(
                    faction, card_type, st.session_state.get("edit_name", "~"))
                st.rerun()

        # — Ability 3 (slot 2) —
        ab2c, ab2b = st.columns([5, 1])
        with ab2c: st.text_area("③ Extra Effect (Legendary / optional)", key="edit_ab2", height=90)
        with ab2b:
            if _regen_btn("🔄", "rab2", "Regenerate extra effect"):
                st.session_state["edit_ab2"] = _regen_effect(
                    faction, card_type, st.session_state.get("edit_name", "~"))
                st.rerun()

        st.markdown("---")

        # — Flavor Text —
        flc, flb = st.columns([5, 1])
        with flc: st.text_area("Flavor Text", key="edit_flavor", height=90)
        with flb:
            if _regen_btn("🔄", "rfl", "Regenerate flavor text"):
                st.session_state["edit_flavor"] = random.choice(FACTIONS[faction]["flavor_quotes"])
                st.rerun()

        # — ATK / DEF (Servant only) —
        if card_type == "Servant":
            st.markdown("---")
            atkc, defc, stb = st.columns([2, 2, 1])
            with atkc: st.number_input("ATK", min_value=0, max_value=9999, step=100, key="edit_atk")
            with defc: st.number_input("DEF", min_value=0, max_value=9999, step=100, key="edit_def")
            with stb:
                if _regen_btn("🔄", "rst", "Regenerate ATK/DEF"):
                    atk, def_ = build_atk_def(
                        RARITIES[st.session_state.get("edit_rarity", "Common")],
                        count_cost(st.session_state.get("edit_cost", "{2}")))
                    st.session_state["edit_atk"] = atk
                    st.session_state["edit_def"] = def_
                    st.rerun()

    # ── Art Prompts (full width below) ────────────────────────────────────────
    st.divider()
    st.subheader("🎨 Art Prompts")
    artc, artb = st.columns([5, 1])
    with artc:
        st.text_input("Art Description (drives all 3 prompts)", key="edit_art_desc")
    with artb:
        if _regen_btn("🔄 Regen", "rart", "Regenerate art description from concept"):
            concept_cur = st.session_state.get("sel_concept", "")
            new_art = (concept_cur + ", " if concept_cur else "") + FACTIONS[faction]["art_style"]
            st.session_state["edit_art_desc"] = new_art
            st.rerun()

    card = _card_from_state()
    prompts = build_art_prompts(card)
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("**Midjourney**")
        st.text_area("mj", value=prompts["midjourney"], height=130, key="disp_mj", label_visibility="collapsed")
    with p2:
        st.markdown("**DALL·E 3**")
        st.text_area("dalle", value=prompts["dalle"], height=130, key="disp_dalle", label_visibility="collapsed")
    with p3:
        st.markdown("**Stable Diffusion**")
        st.text_area("sd", value=f"[+] {prompts['sd_pos']}\n\n[-] {prompts['sd_neg']}", height=130, key="disp_sd", label_visibility="collapsed")


def page_game_concepts():
    st.header("📖 Game Concepts")
    section = st.selectbox("Select section", list(GAME_CONCEPTS.keys()))
    st.markdown(GAME_CONCEPTS[section])


def page_ability_library():
    st.header("⚡ Ability Library")
    st.caption(f"{len(ABILITIES)} abilities across 4 categories")

    cats = ["All", "Keyword", "Triggered", "Activated", "Static"]
    cat_sel  = st.selectbox("Filter by category", cats)
    search   = st.text_input("Search by name or faction", "").lower()

    filtered = [a for a in ABILITIES
                if (cat_sel == "All" or a["cat"] == cat_sel)
                and (not search or search in a["name"].lower() or search in a["faction"].lower())]

    st.caption(f"Showing {len(filtered)} abilities")

    for ab in filtered:
        stars = "★" * ab["power"] + "☆" * (5 - ab["power"])
        with st.expander(f"**{ab['name']}** · {ab['cat']} · {stars}"):
            st.markdown(f"**Faction:** {ab['faction']}")
            st.markdown(f"**Rules:** {ab['rules']}")
            st.markdown(f"**Power:** {stars} ({ab['power']}/5)")


def page_faction_guide():
    st.header("🌍 Faction Guide")
    faction_opts = list(FACTION_GUIDE.keys())
    sel = st.selectbox("Select faction", faction_opts)
    data = FACTION_GUIDE[sel]

    st.markdown(f"### Lore")
    st.markdown(data["lore"])

    st.markdown("### Key Figures")
    for fig_name, desc in data["figures"]:
        st.markdown(f"- **{fig_name}** — {desc}")

    st.markdown("### Playstyle")
    st.markdown(data["playstyle"])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Strengths")
        for s in data["strengths"]:
            st.markdown(f"- ✓ {s}")
    with c2:
        st.markdown("### Weaknesses")
        for w in data["weaknesses"]:
            st.markdown(f"- ✗ {w}")

    st.markdown("### How to Beat This Faction")
    st.markdown(data["counter"])


def page_art_director():
    st.header("🎨 Art Director")
    st.caption("Build standalone AI art prompts without generating a full card.")

    faction_opts = list(ART_STYLES.keys())
    faction_sel  = st.selectbox("Faction (art style)", faction_opts)
    type_sel     = st.selectbox("Card Type (composition)", list(COMP_TEMPLATES.keys()))
    concept_in   = st.text_input("Concept", placeholder="e.g. archangel with sword of fire")

    if st.button("🎨 Generate Prompts", type="primary"):
        style = ART_STYLES[faction_sel]
        comp  = COMP_TEMPLATES[type_sel]
        art   = concept_in.strip() or f"{type_sel.lower()} card for {faction_sel}"

        mj = (f"/imagine prompt: {art}, {style['style']}, {comp}, "
              f"{style['lighting']}, {style['palette']}, TCG card art, "
              f"highly detailed, masterpiece --ar 3:4 --v 6 --stylize 750 --quality 2")
        dalle = (f"Create a professional TCG illustration of {art}. "
                 f"Style: {style['style']}, influenced by {style['influences']}. "
                 f"Composition: {comp}. Lighting: {style['lighting']}. "
                 f"Color palette: {style['palette']}. Premium card art quality.")
        sd_pos = f"{art}, {style['style']}, {comp}, {style['lighting']}, {style['palette']}, highly detailed, masterpiece, 8k"
        sd_neg = f"{style['neg']}, deformed, ugly, blurry, watermark, low quality"

        st.divider()
        st.markdown("**Style Guide**")
        st.markdown(f"- **Style:** {style['style']}")
        st.markdown(f"- **Palette:** {style['palette']}")
        st.markdown(f"- **Lighting:** {style['lighting']}")
        st.markdown(f"- **Influences:** {style['influences']}")
        st.divider()

        p1, p2, p3 = st.columns(3)
        with p1:
            st.markdown("**Midjourney**")
            st.text_area("", value=mj, height=150, key="art_mj", label_visibility="collapsed")
        with p2:
            st.markdown("**DALL·E 3**")
            st.text_area("", value=dalle, height=150, key="art_dalle", label_visibility="collapsed")
        with p3:
            st.markdown("**Stable Diffusion**")
            st.text_area("", value=f"[+] {sd_pos}\n\n[-] {sd_neg}", height=150, key="art_sd", label_visibility="collapsed")


# ────────────────────────────────────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────────────────────────────────────

def main():
    css()

    with st.sidebar:
        st.markdown("## ✦ TESTAMENT")
        st.markdown("*TCG Card Generation Engine*")
        st.divider()
        page = st.radio(
            "Navigate",
            ["🃏 Card Generator", "📖 Game Concepts", "⚡ Ability Library", "🌍 Faction Guide", "🎨 Art Director"],
            label_visibility="collapsed",
        )
        st.divider()
        st.markdown("**6 Factions · 7 Card Types**")
        st.markdown("**64 Abilities · 4 Rarities**")
        st.markdown("**Midjourney · DALL·E · SD**")
        st.divider()
        st.caption("Cards saved locally on download.")

    if page == "🃏 Card Generator":     page_generator()
    elif page == "📖 Game Concepts":    page_game_concepts()
    elif page == "⚡ Ability Library":  page_ability_library()
    elif page == "🌍 Faction Guide":    page_faction_guide()
    elif page == "🎨 Art Director":     page_art_director()


if __name__ == "__main__":
    main()
