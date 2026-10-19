// v0.14.1 micro-patch: move acquired skill icon below Timing Square.
(function(){
  const originalDrawSkillIcon = drawSkillIcon;
  drawSkillIcon = function(now){
    const g = squareGeom();
    ctx.save();
    ctx.translate(0, g.size + 51);
    originalDrawSkillIcon(now);
    ctx.restore();
  };
})();
