import Lean
run_cmd do
  let _ ← IO.eprintln "68 diagnostic direct IO marker"
  pure ()
