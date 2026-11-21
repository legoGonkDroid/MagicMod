// Hide the vanilla recipe book outside creative mode
//
// Removes the green recipe-book button from the inventory, crafting table and furnace-type
// screens, and keeps the recipe book panel closed, unless the player is in creative mode.
// EMI stays available for looking up recipes. (Vanilla and EMI have no option for this:
// EMI's recipe-book-action setting only changes what the button does.)
//
// Client-side only; does nothing on a dedicated server. Native NeoForge listeners, so this
// lives in startup_scripts and needs a full game restart after edits.

if (Platform.isClientEnvironment()) {
  var $ScreenOpening = Java.loadClass('net.neoforged.neoforge.client.event.ScreenEvent$Opening')
  var $ScreenInitPost = Java.loadClass('net.neoforged.neoforge.client.event.ScreenEvent$Init$Post')
  var $RecipeUpdateListener = Java.loadClass('net.minecraft.client.gui.screens.recipebook.RecipeUpdateListener')
  var $RecipeBookType = Java.loadClass('net.minecraft.world.inventory.RecipeBookType')
  var $Minecraft = Java.loadClass('net.minecraft.client.Minecraft')
  var $ImageButton = Java.loadClass('net.minecraft.client.gui.components.ImageButton')

  var hideRecipeBookActive = () => {
    var player = $Minecraft.getInstance().player
    return player != null && !player.isCreative()
  }

  // Errors are logged instead of thrown: an exception in a screen event crashes the game.

  // Before the screen builds its layout: make sure the recipe book panel starts closed,
  // so the screen is centred normally.
  NativeEvents.onEvent($ScreenOpening, event => {
    try {
      if (!(event.getNewScreen() instanceof $RecipeUpdateListener) || !hideRecipeBookActive()) return
      var book = $Minecraft.getInstance().player.getRecipeBook()
      var types = $RecipeBookType.values()
      for (var i = 0; i < types.length; i++) book.setOpen(types[i], false)
    } catch (err) {
      console.error('[hide_recipe_book] opening: ' + err)
    }
  })

  // After the screen adds its widgets: remove the recipe book button, which vanilla adds as
  // a 20x18 ImageButton on these screens. (KubeJS blocks getClass(), so match by
  // instanceof + size.)
  NativeEvents.onEvent($ScreenInitPost, event => {
    try {
      if (!(event.getScreen() instanceof $RecipeUpdateListener) || !hideRecipeBookActive()) return
      var widgets = event.getListenersList().toArray()
      for (var i = 0; i < widgets.length; i++) {
        var w = widgets[i]
        if (!(w instanceof $ImageButton)) continue
        if (w.getWidth() === 20 && w.getHeight() === 18) event.removeListener(w)
      }
    } catch (err) {
      console.error('[hide_recipe_book] init: ' + err)
    }
  })
}
