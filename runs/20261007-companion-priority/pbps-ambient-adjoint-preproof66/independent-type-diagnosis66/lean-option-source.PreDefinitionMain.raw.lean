                  m!"fail to show termination for{indentD (MessageData.joinSep preDefMsgs Format.line)}\nwith errors\n{msg}")
          catch ex =>
            logException ex
            let s ← saveState
            try
              if preDefs.all fun preDef => (preDef.kind matches DefKind.def | DefKind.instance) || preDefs.all fun preDef => preDef.kind == DefKind.abbrev then
                -- try to add as partial definition
                withOptions (Elab.async.set · false) do
                  try
                    addAndCompilePartial docCtx preDefs (useSorry := true)
                  catch _ =>
                    -- Compilation failed try again just as axiom
