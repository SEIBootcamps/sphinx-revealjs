import { basename, extname } from "path";
import postcss from "rollup-plugin-postcss";


// Base directories
const assetsDir = "src/sphinx_revealjs_slides/theme/assets";
const outputDir = "src/sphinx_revealjs_slides/theme/revealjs/static";

// Configuration for entry points - can be extended in the future
const entryPoints = {
  js: [`${assetsDir}/scripts/main.js`],
  css: [`${assetsDir}/styles/main.css`],
};

// Generate output configuration for JS files
function createJsConfig(input, index) {
  const name = basename(input, extname(input));
  return {
    input,
    output: {
      file: `${outputDir}/${name}.js`,
      format: "iife",
      sourcemap: true,
    },
  };
}

// Generate output configuration for CSS files
function createCssConfig(input, index) {
  const name = basename(input, extname(input));
  return {
    input,
    plugins: [
      postcss({
        extract: `${name}.css`,
        minimize: false,
      }),
    ],
    output: {
      file: `${outputDir}/${name}.js`, // Dummy output, CSS is extracted separately
      format: "es",
    },
    onwarn(warning, warn) {
      // Suppress warnings about empty bundles (CSS only)
      if (warning.code === "EMPTY_BUNDLE") return;
      warn(warning);
    },
  };
}

// Build configuration array
const config = [
  ...entryPoints.js.map((entry, index) => createJsConfig(entry, index)),
  ...entryPoints.css.map((entry, index) => createCssConfig(entry, index)),
];

export default config;
