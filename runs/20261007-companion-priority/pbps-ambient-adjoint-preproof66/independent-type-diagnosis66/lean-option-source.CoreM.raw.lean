register_builtin_option Elab.async : Bool := {
  defValue := false
  descr := "perform elaboration using multiple threads where possible\
    \n\
    \nThis option defaults to `false` but (when not explicitly set) is overridden to `true` in \
      the Lean language server and cmdline. \
      Metaprogramming users driving elaboration directly via e.g. \
      `Lean.Elab.Command.elabCommandTopLevel` can opt into asynchronous elaboration by setting \
      this option but then are responsible for processing messages and other data not only in the \
      resulting command state but also from async tasks in `Lean.Command.Context.snap?` and \
      `Lean.Command.State.snapshotTasks`."
