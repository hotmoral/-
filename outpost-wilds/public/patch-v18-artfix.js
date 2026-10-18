/* V18 authored transparent SVG asset binding. Runs after patch-v18. */
for(const [key,oldPath] of Object.entries(V18_ASSET_PATHS)){
  const svgPath=oldPath.replace(/\.png$/i,'.svg');
  V18_ASSET_PATHS[key]=svgPath;
  if(v18Assets[key])v18Assets[key].src=svgPath;
}
