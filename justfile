build *opts: (_sphinx "sphinx-build" "revealjs" "example" "example" join("example", "_build") opts)
build_html *opts: (_sphinx "sphinx-build" "html" "example" "example" join("example", "_build") opts)

_sphinx cmd builder config source output *opts:
  @echo "Using {{cmd}} to build {{source}}"
  {{cmd}} \
    -b {{builder}} \
    -d {{output}}/doctrees \
    -n \
    -c {{config}} \
    {{opts}} \
    {{source}} {{join(output, builder)}}
  @echo "Opening in browser..."
  open {{join(output, builder, "index.html")}}