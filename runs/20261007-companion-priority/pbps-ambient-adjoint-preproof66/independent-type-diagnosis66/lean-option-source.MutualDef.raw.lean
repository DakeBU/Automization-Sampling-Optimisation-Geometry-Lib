        if header.kind == .instance then
          if !(← isProp header.type) then
            setReducibilityStatus header.declName .instanceReducible

    if let (#[view], #[declId]) := (views, expandedDeclIds) then
      if Elab.async.get (← getOptions) && view.kind.isTheorem &&
          !deprecated.oldSectionVars.get (← getOptions) &&
          -- holes in theorem types is not a fatal error, but it does make parallelism impossible
          !headers[0]!.type.hasMVar then
        elabAsync headers[0]! view declId
      else elabSync headers
    else elabSync headers

    -- Warn about class-typed `def`s that aren't marked with a reducibility attribute.
