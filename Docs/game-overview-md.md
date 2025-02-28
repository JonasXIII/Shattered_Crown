# Chronicles of the Shattered Crown

## Core Concept
A medieval open-world RPG where you explore a fractured kingdom overrun by monsters, bandits, and dark magic. Travel between towns to gather quests, delve into procedurally generated dungeons/forests/castles, and fight tactical turn-based battles on a grid. Upgrade your gear, recruit companions, and uncover the mystery of the Shattered Crown artifact.

## Key Mechanics

### World Structure
- **Overworld Map**
  - A pixel-art top-down map of the kingdom with towns, forests, mountains, ruins, etc.
  - Travel between locations risks random encounters (e.g., ambushes, merchants, events)
- **Local Areas**
  - Enter specific tiles (e.g., "Haunted Forest" or "Bandit Fort") to load a grid-based level
  - Quests are tied to these areas (e.g., "Clear the spider infestation in the Old Mine")

### Movement & Exploration
- **Grid-Based Maps**
  - Hex grids for organic movement (or square grids if prioritizing simplicity)
  - Each action (move, attack, use skill) costs Action Points (AP)
  - Example: Move 1 hex = 1 AP, Basic Attack = 2 AP, Powerful Skill = 3 AP + cooldown
- **Fog of War**: Unexplored areas are hidden, rewarding scouting

### Combat System
- **Turn-Based Tactics**
  - Enemies include bandits, wolves, undead, vampires, and more, each with unique abilities:
    - Wolves: Pack tactics (bonus damage when adjacent to allies)
    - Vampires: Lifesteal on attacks
    - Skeletons: Resurrect once unless killed with holy damage
  - Terrain matters: Hide behind trees for cover, light oil spills on fire, etc.
- **Class System**: Choose a starting class with unique skills:
  - Knight: Tank with shield bash and taunt
  - Ranger: Ranged attacks and traps
  - Mage: Fireballs, healing, and curses
  - Rogue: Stealth backstabs and poison

### Progression
- **Skill Trees**: Unlock abilities (e.g., "Dragon Slayer" for bonus damage vs. drakes)
- **Gear Crafting**: Collect loot (ore, pelts, monster parts) to forge weapons/armor in towns
- **Companions**: Recruit NPCs (e.g., a warhound, a disgraced paladin) with their own skill sets

### Quests & Economy
- **Town Hubs**: Accept quests from villagers (e.g., "Rescue my child from cultists")
- **Reputation system**: Help towns to unlock better gear/quests
- **Dynamic Events**: While traveling, you might stumble upon a caravan under attack or a cursed shrine

## Art Style & Tone
- **Pixel Art**: Retro 16-bit inspired (think Stardew Valley meets Final Fantasy Tactics)
- **Atmosphere**: Moody but adventurous – dark forests, candlelit crypts, and stormy castles

## Example Gameplay Flow
1. **Overworld**: Travel from "Riverhelm Village" to the "Cursed Bog" tile
2. **Local Area**: Load a hex-grid swamp map with fog of war
3. **Combat**: Fight vampire spawn and giant spiders. Use the mage's fire spell to ignite gas vents
4. **Loot**: Find a "Vampiric Dagger" (+lifesteal) and a quest item (cultist ledger)
5. **Return to Town**: Craft better armor, recruit a cleric, and accept a new quest
