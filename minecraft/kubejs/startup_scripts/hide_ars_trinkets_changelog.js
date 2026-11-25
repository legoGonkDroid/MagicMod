// Suppress Ars Trinkets' "what's new" changelog chat message on login
//
// Ars Trinkets (ChangelogLoginEvents) prints its changelog on PlayerLoggedInEvent unless the
// player's persistent data has PlayerPersisted.ars_trinkets_changelog_seen == the mod version.
// There is no config toggle, so this listener runs first (HIGHEST priority) and marks the
// current version as already seen.
//
// Native NeoForge listener: lives in startup_scripts, needs a full game restart after edits.
// Rhino notes: `$`-prefixed class handles, `var` inside functions.

const $ChangelogEventPriority = Java.loadClass('net.neoforged.bus.api.EventPriority')
const $PlayerLoggedInEvent = Java.loadClass('net.neoforged.neoforge.event.entity.player.PlayerEvent$PlayerLoggedInEvent')

NativeEvents.onEvent($ChangelogEventPriority.HIGHEST, $PlayerLoggedInEvent, event => {
  try {
    // KubeJS's class filter blocks net.neoforged.fml.ModList; Platform wraps the same version.
    if (!Platform.isLoaded('ars_trinkets')) return
    var version = String(Platform.getInfo('ars_trinkets').getVersion())
    var data = event.getEntity().getPersistentData()
    var persisted = data.getCompound('PlayerPersisted')
    persisted.putString('ars_trinkets_changelog_seen', version)
    data.put('PlayerPersisted', persisted)
  } catch (err) {
    console.error('[hide_ars_trinkets_changelog] ' + err)
  }
})
