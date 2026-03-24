// ============================================================
//  db.js — Live data from Flask API
//  Replaces the old static db.js
//  All pages include this script; it fetches once and sets:
//    • processorDB      – raw array from API
//    • rankedProcessors – sorted by nanoScore with rank added
//    • processorMap     – { name: processor } lookup
// ============================================================

const API_URL = 'http://127.0.0.1:5000/api/processors';

// Global variables (same names the HTML pages already use)
let processorDB      = [];
let rankedProcessors = [];
let processorMap     = {};

// ── Fetch and build globals ───────────────────────────────────
async function loadProcessors() {
  try {
    const res  = await fetch(API_URL);
    const data = await res.json();

    // Normalise field names: API uses "nanoscore", HTML uses "nanoScore"
    processorDB = data.map(p => ({
      id:        p.id,
      name:      p.name,
      company:   p.company,
      cpu:       p.cpu,
      gpu:       p.gpu,
      battery:   p.battery,
      nanoScore: p.nanoscore,   // ← normalise here
      antutu:    p.antutu  || 0,
      process:   p.process || 'N/A',
      pros:      Array.isArray(p.pros) ? p.pros : []
    }));

    // Sort by nanoScore descending and add rank
    rankedProcessors = [...processorDB]
      .sort((a, b) => b.nanoScore - a.nanoScore)
      .map((p, i) => ({ ...p, rank: i + 1 }));

    // Build name → processor map
    processorMap = {};
    rankedProcessors.forEach(p => { processorMap[p.name] = p; });

    // Fire a custom event so each page knows data is ready
    document.dispatchEvent(new Event('dbReady'));

  } catch (err) {
    console.error('ProcBench: failed to load processors from API', err);
    document.dispatchEvent(new CustomEvent('dbError', { detail: err }));
  }
}

// Start loading immediately when this script is included
loadProcessors();
