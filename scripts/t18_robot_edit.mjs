import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const SRC = '/home/z/my-project/upload/ChatGPT Image Sep 11, 2026, 02_17_38 PM.png';
const OUT = '/home/z/my-project/upload/robot_avatar.png';

const PROMPT = `Transform this person into a friendly cute 3D robot mascot character for a mobile app. Keep subtle recognizable features of the person integrated into the robot design: short dark hair silhouette, round glasses shape on the robot's visor, and a small beard hint on the faceplate. The robot head and shoulders face DIRECTLY FORWARD, looking STRAIGHT AT THE VIEWER with big glowing cyan eyes. Sleek white and deep-purple metal panels with glowing cyan accents, small antenna with glowing tip. Centered symmetrical portrait, dark purple gradient background, soft rim lighting, polished high-quality 3D render, app mascot style`;

async function main() {
  const zai = await ZAI.create();
  const b64 = fs.readFileSync(SRC).toString('base64');
  const dataUrl = 'data:image/png;base64,' + b64;
  let done = false;
  for (let attempt = 1; attempt <= 3 && !done; attempt++) {
    try {
      const res = await zai.images.generations.edit({
        prompt: PROMPT,
        images: [{ url: dataUrl }],
        size: '1024x1024'
      });
      const out = res && res.data && res.data[0] && res.data[0].base64;
      if (!out) throw new Error('empty response');
      fs.writeFileSync(OUT, Buffer.from(out, 'base64'));
      console.log('OK bytes:', fs.statSync(OUT).size);
      done = true;
    } catch (e) {
      console.error('attempt', attempt, 'failed:', e.message);
      if (attempt < 3) await new Promise(r => setTimeout(r, 1500 * attempt));
      else throw e;
    }
  }
}

main().catch(e => { console.error('FATAL', e.message); process.exit(1); });
