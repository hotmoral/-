set -euo pipefail
check() {
  actual="$(git hash-object "$APP/$1")"
  test "$actual" = "$2" || { echo "$1 $actual != $2"; exit 1; }
}
check package.json b0f0d0f19540ab16f3818df62de30e113b0147c7
check src/app.mjs f13819f925add4eb52f464ff58a626c4d438d9e6
check src/clear-result-ui.mjs c9235254d396661d26fc793e74c1d68282af2790
check src/polish.mjs d9efb1a0640fd9dc9a879462dc66ede216f8ff0f
check src/visual-assets.mjs 667ef92c5268cf684d187dd335877083efbffa2a
check src/settings-preferences.mjs 22450f785bdbd3b29bbe87b0ef93ced054898b45
check src/settings-about.mjs 3c59b9e6a16d3b904221a89218748bf887516d27
check assets/performance-stamps/s-plus-approved.svg 20b99b53cc61ec63b40e9c9d6dc0555a52c5d7c6
check assets/performance-stamps/a-plus-approved.svg 1c298ff9dcee1ec4e28cbb583ce7ef7000d171f8
check assets/performance-stamps/b-plus-approved.svg fdf0fd885b4effa92c94260bb9f9bce3b1258b5a
check tests/foundation.test.mjs c0ecbe79cd32f8c178edc4010e61331c21822c4f
check tests/progress-reset.test.mjs b92979e9f83260b834fe4bc7fc0b269a71497da8
check tests/settings-preferences.test.mjs a40813a76229ad398e5b6af1d5caf39dd872ee49
check tests/settings-about.test.mjs 459328837383fba4fd98b460226c264be72f21df
check tests/performance-stamp.test.mjs 0819d510082f855eb2663c84d10443aa75954111
check tests/clear-outcome.test.mjs d61d43822c57378ac4ae58bbeb017ebb771d68ee
check tests/runtime.test.mjs 251f703a6fe8771dd294cf6d372ffd32922b8dcd
check tests/navigation.test.mjs 3de440371beafa73a3f13824a62b368c9c759457
check tests/path-geometry.test.mjs 8e61fcfd802e26f459a1307fded5fbe5dd01903c
check tests/polish.test.mjs 0d041dded7b87ae89f967c0823af1f3949b1cc07
