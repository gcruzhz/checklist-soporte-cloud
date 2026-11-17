const sharp = require('sharp');
const fs = require('fs');
(async () => {
  const svg = fs.readFileSync('assets/icon-source.svg', 'utf8');
  const cham = await sharp(Buffer.from(svg)).resize(1700, 1700, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } }).png().toBuffer();
  await sharp({ create: { width: 2732, height: 2732, channels: 4, background: { r: 255, g: 255, b: 255, alpha: 1 } } })
    .composite([{ input: cham, gravity: 'centre' }]).png().toFile('assets/splash.png');
  const svgLight = svg.replace(/#0C322C/gi, '#73BA25');
  const chamLight = await sharp(Buffer.from(svgLight)).resize(1700, 1700, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } }).png().toBuffer();
  await sharp({ create: { width: 2732, height: 2732, channels: 4, background: { r: 12, g: 50, b: 44, alpha: 1 } } })
    .composite([{ input: chamLight, gravity: 'centre' }]).png().toFile('assets/splash-dark.png');
  console.log('splash OK');
})();
