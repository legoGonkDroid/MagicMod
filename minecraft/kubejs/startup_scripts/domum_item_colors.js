// Fix Domum Ornamentum inventory icons ignoring the materials they were cut from
//
// Domum colours its items through NeoForge's BakedModel#getRenderPasses(ItemStack). Continuity
// (emissive textures, which Ars Lumos/Ars Elemental/Supplementaries rely on for their glow)
// wraps every baked model in an EmissiveBakedModel that is not a "vanilla adapter". Sodium's
// Fabric-renderer item path then draws such models itself via emitItemQuads and never calls
// getRenderPasses, so Domum items fall back to their untextured default model. Placed blocks
// are unaffected (they use ModelData, which the wrapper forwards).
//
// After Continuity has wrapped the models (LOWEST priority), unwrap only Domum's *item*
// (`#inventory`) models. Blocks and every other mod keep Continuity's emissive wrapping.
//
// Client-only, native mod-bus listener: lives in startup_scripts, needs a full restart after edits.
// Rhino notes: `var` inside blocks, `$`-prefixed class handles, try/catch around the handler.

if (Platform.isClientEnvironment() && Platform.isLoaded('continuity') && Platform.isLoaded('domum_ornamentum')) {
  var $DomumEventPriority = Java.loadClass('net.neoforged.bus.api.EventPriority')
  var $ModifyBakingResult = Java.loadClass('net.neoforged.neoforge.client.event.ModelEvent$ModifyBakingResult')

  NativeEvents.onEvent($DomumEventPriority.LOWEST, $ModifyBakingResult, event => {
    try {
      // Load Continuity's class HERE, not at script load: loading it at startup runs its static
      // setup, which initialises Continuity's RenderUtil before Minecraft has a ModelManager.
      // RenderUtil keeps the null, the first resource reload throws an NPE, and startup hangs.
      // By this event Continuity has already created EmissiveBakedModels, so this is safe.
      var $EmissiveBakedModel = Java.loadClass('me.pepperbell.continuity.client.model.EmissiveBakedModel')
      var models = event.getModels()
      var keys = models.keySet().toArray()
      var unwrapped = 0
      for (var i = 0; i < keys.length; i++) {
        var key = keys[i]
        if (String(key.id().getNamespace()) !== 'domum_ornamentum' || String(key.variant()) !== 'inventory') continue
        var model = models.get(key)
        var changed = false
        while (model instanceof $EmissiveBakedModel) {
          model = model.getWrappedModel()
          changed = true
        }
        if (changed) {
          models.put(key, model)
          unwrapped++
        }
      }
      console.info('[domum_item_colors] unwrapped ' + unwrapped + ' Domum Ornamentum item models')
    } catch (err) {
      console.error('[domum_item_colors] ' + err)
    }
  })
}
