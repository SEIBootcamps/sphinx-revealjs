build: (_sphinx "sphinx-build" "revealjs" "example" "example" join("example", "_build"))

_sphinx cmd builder config source output *opts:
  @echo "Using {{cmd}} to build {{source}}"
  poetry run {{cmd}} \
    -b {{builder}} \
    -d {{output}}/doctrees \
    -n \
    -c {{config}} \
    {{opts}} \
    {{source}} {{join(output, builder)}}
  @echo "Opening in browser..."
  open {{join(output, builder, "index.html")}}