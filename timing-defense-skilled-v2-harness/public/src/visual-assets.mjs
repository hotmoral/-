import './visual-assets-v52-core.mjs';

const weightStyle = document.createElement('style');
weightStyle.dataset.linklineVisualWeight = 'v5.4';
weightStyle.textContent = `
.visual-chain-body,.slide-chain-body{stroke-width:5.70!important}
`;
document.head.append(weightStyle);

// Linkline visual asset entry v5.4: accepted v5.2 motion core with doubled chain body stroke only; nodes remain unchanged.
