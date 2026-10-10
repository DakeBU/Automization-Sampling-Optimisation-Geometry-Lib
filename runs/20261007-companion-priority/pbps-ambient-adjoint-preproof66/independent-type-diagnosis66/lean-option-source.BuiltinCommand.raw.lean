    let mut lines : Array MessageData := #[]
    let decls ← getOptionDecls
    for (name, val) in opts do
      -- `#guard_msgs` sets this option internally, we don't want it to end up in its output
      if name == `Elab.async then
        continue
      let (isSet, isUnknown) :=
        match decls.find? name with
        | some decl => (decl.defValue != val, false)
