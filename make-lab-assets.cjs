const sharp = require('sharp');
(async () => {
  const src = 'assets/media-generation-lab-icon-0-9870ef0c-6cfd-4101-af85-a2b47de33776.webp';
  const meta = await sharp(src).metadata();
  console.log('origen:', meta.width, 'x', meta.height, meta.format);
  const icon = await sharp(src).resize(1024, 1024, { fit: 'contain', background: { r: 255, g: 255, b: 255, alpha: 1 } }).png().toBuffer();
  await sharp(icon).toFile('assets/icon.png');
  await sharp(icon).toFile('www/lab-icon.png');
  const splashLogo = await sharp(icon).resize(1500, 1500, { fit: 'contain', background: { r: 255, g: 255, b: 255, alpha: 1 } }).png().toBuffer();
  const canvas = { create: { width: 2732, height: 2732, channels: 4, background: { r: 255, g: 255, b: 255, alpha: 1 } } };
  await sharp(canvas).composite([{ input: splashLogo, gravity: 'centre' }]).png().toFile('assets/splash.png');
  await sharp(canvas).composite([{ input: splashLogo, gravity: 'centre' }]).png().toFile('assets/splash-dark.png');
  console.log('lab assets OK');
})();
