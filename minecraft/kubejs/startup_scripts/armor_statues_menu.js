// Armor Statues menu on empty-hand sneak + right-click
//
// Armor Statues opens its statue menu on sneak + right-click with an empty hand, but
// Armor Quick Swap listens for the same click and was winning (it swapped armor instead).
// This listener runs first (HIGHEST priority), opens the menu through Armor Statues' own
// handler (so its rules still apply: empty hand, may build, invulnerable stands need
// creative), and cancels the click so Armor Quick Swap never sees it.
// Sneak + right-click while holding an item is left alone -> Armor Quick Swap swaps armor.
//
// Native NeoForge listener: lives in startup_scripts, needs a full game restart after edits.
// Rhino notes: `$`-prefixed class handles (KubeJS predefines some globals), `var` inside
// functions, no template strings/destructuring.

const $EventPriority = Java.loadClass('net.neoforged.bus.api.EventPriority')
const $EntityInteractSpecific = Java.loadClass('net.neoforged.neoforge.event.entity.player.PlayerInteractEvent$EntityInteractSpecific')
const $ArmorStand = Java.loadClass('net.minecraft.world.entity.decoration.ArmorStand')
const $ArmorStatuesInteractHandler = Java.loadClass('fuzs.armorstatues.handler.ArmorStandInteractHandler')

NativeEvents.onEvent($EventPriority.HIGHEST, $EntityInteractSpecific, event => {
  var player = event.getEntity()
  var stand = event.getTarget()
  if (event.getLevel().isClientSide()) return
  // Compare enums by name: Rhino wraps Java enums, so identity checks are unreliable.
  if (String(event.getHand().name()) !== 'MAIN_HAND') return
  if (!(stand instanceof $ArmorStand)) return
  if (!player.isShiftKeyDown() || stand.isMarker() || player.isSpectator()) return
  if (!player.getMainHandItem().isEmpty()) return

  try {
    var opened = $ArmorStatuesInteractHandler.onUseEntityAt(player, event.getLevel(), event.getHand(), stand, event.getLocalPos())
    if (opened.isInterrupt()) {
      event.setCancellationResult(opened.getInterrupt().get())
      event.setCanceled(true)
    }
  } catch (err) {
    console.error('[armor_statues_menu] ' + err)
  }
})
