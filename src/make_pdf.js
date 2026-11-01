// Render build/*.html to PDFs in the repo root:  node src/make_pdf.js
const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const JOBS = [
  ['build/student-booklet.html', 'Algebra-Basic-Skills-Booklet.pdf', 'Algebra Basic Skills'],
  ['build/teacher-answer-key.html', 'Algebra-Basic-Skills-Teacher-Answer-Key.pdf', 'Teacher Answer Key'],
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push(String(e)));
  for (const [src, out, label] of JOBS) {
    await page.goto('file://' + path.join(ROOT, src));
    await page.emulateMedia({ media: 'print' });
    await page.pdf({
      path: path.join(ROOT, out),
      format: 'A4',
      printBackground: true,
      margin: { top: '12mm', bottom: '14mm', left: '12mm', right: '12mm' },
      displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate: `<div style="font-size:8px;color:#777;width:100%;padding:0 12mm;display:flex;justify-content:space-between;font-family:Arial,sans-serif"><span>${label}</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>`,
    });
    console.log('Wrote', out);
  }
  await browser.close();
  if (errors.length) { console.error('Console errors:', errors); process.exit(1); }
})();
