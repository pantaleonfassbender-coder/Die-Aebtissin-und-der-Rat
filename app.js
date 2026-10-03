/* Die Äbtissin und der Rat. Caritas Pirckheimer und das Nürnberger Klarakloster 1524–1528 — ein Quellenapparat. Vanilla JS, Hash-Routen. */
"use strict";

const view = document.getElementById("view");
const D = { mods: null, plates: null, timeline: null, compare: null, texts: {} };
const SIDES = { konvent: "Die Äbtissin und der Konvent", rat: "Der Rat und der Pfleger", familien: "Die Familien", reform: "Prediger und Reformatoren", nachwelt: "Gelehrte und Nachwelt" };
const LANGS = { la: "Latein", gmh: "Mittelhochdeutsch", fnhd: "Frühneuhochdeutsch", de: "Deutsch", en: "Übersetzung" };

const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const side = s => `<span class="side ${s}">${esc(SIDES[s] || s)}</span>`;
const plateOf = id => (D.plates.plates || []).find(p => p.id === id);
const getJSON = url => fetch(url).then(r => { if (!r.ok) throw new Error(url); return r.json(); });

let langPref = "both";
try { langPref = localStorage.getItem("klara_lang") || "both"; } catch (e) { /* storage blocked */ }

async function boot() {
  [D.mods, D.plates, D.timeline, D.compare] = await Promise.all(
    ["data/modules.json", "data/plates.json", "data/timeline.json", "data/compare.json"].map(getJSON));
  document.getElementById("navCompare").hidden = !(D.compare.pairs || []).length;
  document.getElementById("navPlates").hidden = !(D.plates.plates || []).length;
  window.addEventListener("hashchange", route);
  route();
}

async function text(id) {
  if (!D.texts[id]) D.texts[id] = await getJSON(`data/${id}.json`);
  return D.texts[id];
}

function route() {
  const parts = (location.hash.replace(/^#\/?/, "") || "").split("/").filter(Boolean);
  const [page, ...args] = parts;
  document.querySelectorAll(".top nav a").forEach(a => {
    const t = a.getAttribute("href").replace(/^#\/?/, "");
    a.classList.toggle("on", (t || "") === (page === "text" ? "texts" : page || ""));
  });
  view.innerHTML = "";
  window.scrollTo(0, 0);
  const pages = { "": overview, texts, text: reader, compare, timeline, plates, sources };
  (pages[page || ""] || overview)(args);
}

/* ------------------------------------------------------------ overview */
function overview() {
  view.innerHTML = `
  <div class="hero one">
    <div>
      <span class="tag">1524–1528 · Nürnberg · die Äbtissin · der Rat · die Familien</span>
      <h1>Die Äbtissin und der Rat</h1>
      <p class="lede">1525 führte der Rat der Reichsstadt Nürnberg die Reformation ein. Im Klarakloster lebten Schwestern aus den ersten Familien der Stadt, Töchter und Schwestern eben dieses Rats; ihre Äbtissin war Caritas Pirckheimer, die Schwester des Humanisten Willibald Pirckheimer, eine gelehrte Frau, mit der die Humanisten Briefe wechselten. Der Rat nahm den Schwestern die Franziskaner als Beichtväter und schickte ihnen lutherische Prediger; Mütter holten ihre Töchter gegen deren Willen heraus; Philipp Melanchthon kam ans Redefenster. Caritas schrieb alles auf: ihre Bittschriften, die Briefe hin und her, die Antworten, die ausblieben. Novizinnen durfte das Kloster nicht mehr aufnehmen. Aufgelöst wurde es nie; es lebte, bis 1596 die letzte Schwester starb.</p>
      <p class="readable">Dieser Apparat folgt dem Streit durch die Aufzeichnungen der Äbtissin, ihre Denkwürdigkeiten, in der gemeinfreien Ausgabe von 1852, das frühneuhochdeutsche Original neben einer neuhochdeutschen Arbeitsübersetzung, dazu die Briefe der Humanisten an die gelehrte Äbtissin, die Stimmen der Reformatoren und die Chronik vom Ende des Klosters.</p>
    </div>
  </div>

  <h2>Was der Apparat enthält</h2>
  ${D.mods.shipped.length ? `<div class="grid g2">${D.mods.shipped.map(card).join("")}</div>` : `<p class="fine">Die ersten Module sind in Arbeit; die Seite „Texte“ nennt sie mit ihren Quellen.</p>`}

  <h2>Die Fragen</h2>
  <div class="grid g2">
    <div class="panel"><h3>Wem gehören die Schwestern?</h3>
      <p>Ihren Familien, die sie als Mädchen ins Kloster gegeben hatten und nun mit dem Evangelium zurückforderten; dem Rat, der über das Kloster gebot; oder sich selbst und ihrem Gelübde? Caritas’ Antwort: Sie gegen ihren Willen hinauszutreiben, „wer nit evangelisch“.</p></div>
    <div class="panel"><h3>Was kann eine Äbtissin gegen einen Rat?</h3>
      <p>Keine Waffen, kein Gericht, kaum einen Fürsprecher: nur Bittschriften, Briefe, das Gespräch am Redefenster, Geduld und die Einigkeit ihres Konvents. Der Apparat zeigt, wie weit das trug.</p></div>
    <div class="panel"><h3>Wer übte Gewalt, und wer nannte sie so?</h3>
      <p>Die Mütter, die ihre Töchter aus dem Kloster ziehen ließen, beriefen sich auf ihr Gewissen; die Töchter riefen auf der Straße, man tue ihnen Gewalt und Unrecht. Der Apparat erzählt beides und nennt auch, was das Kloster selbst von Mädchen verlangte, die es als Kinder aufnahm.</p></div>
    <div class="panel"><h3>Lässt sich das spielen?</h3>
      <p>Ein Begleitspiel, <em>Verhört man doch einen Dieb</em>, ist in Vorbereitung: Man spielt die Äbtissin, von 1524 bis 1528, mit einem Epilog bis 1596. Seine Karten werden auf die Stellen verweisen, die hier abgedruckt sind.</p></div>
  </div>`;
}

function card(m) {
  return `<a class="card" href="#/text/${m.id}">
    <div>${side(m.side)} <span class="fine">${esc(m.zk)}</span></div>
    <h3>${esc(m.kurz)}</h3><p class="fine">${esc(m.warum)}</p></a>`;
}

/* ------------------------------------------------------------ texts */
function texts() {
  view.innerHTML = `
    <span class="tag">Texte</span><h1>Das Korpus</h1>
    <p class="lede">Jedes Modul ist vollständig lesbar, das Original neben der Übersetzung. Geplante Module nennen ihre Quellen; was geprüft und nicht aufgenommen wurde, steht unten mit Begründung.</p>
    ${D.mods.shipped.length ? `<h2>Abgedruckt</h2><div class="grid g2">${D.mods.shipped.map(card).join("")}</div>` : ""}
    ${(D.mods.planned || []).length ? `<h2>Geplant</h2><div class="grid g2">${D.mods.planned.map(m => `
      <div class="card planned"><div>${side(m.side)} <span class="fine">geplant</span></div>
      <h3>${esc(m.kurz)}</h3><p class="fine">${esc(m.warum)}</p><p class="fine"><b>Quelle:</b> ${esc(m.quelle)}</p></div>`).join("")}</div>` : ""}
    ${(D.mods.missing || []).length ? `<h2 id="missing">Geprüft und nicht aufgenommen</h2><div class="grid g2">${D.mods.missing.map(m => `
      <div class="card planned"><div>${side(m.side)} <span class="fine">nicht aufgenommen</span></div>
      <h3>${esc(m.kurz)}</h3><p class="fine">${esc(m.warum)}</p><p class="fine"><b>Quelle:</b> ${esc(m.quelle)}</p></div>`).join("")}</div>` : ""}`;
}

async function reader([id, secId, unitN]) {
  const m = D.mods.shipped.find(x => x.id === id);
  if (!m) { location.hash = "#/texts"; return; }
  view.innerHTML = `<p class="fine">Wird geladen…</p>`;
  const t = await text(m.datei);
  const sec = t.sections.find(s => s.id === secId) || t.sections[0];
  const bilingual = sec.units.some(u => u.orig);
  const lang = bilingual ? langPref : "en";
  const langs = [...new Set(sec.units.filter(u => u.orig).map(u => u.lang || t.orig_sprache))];
  const origName = langs.length === 1 ? (LANGS[langs[0]] || "Original") : langs.length === 2 ? langs.map(l => LANGS[l] || l).join(" oder ") : "Original";
  view.innerHTML = `
    <p class="fine"><a href="#/texts">← Alle Texte</a></p>
    <span class="tag">${side(m.side)} ${esc(t.jahr)} · zitiert als ${esc(sec.zk)} [n]</span>
    <h1>${esc(t.titel)}</h1>
    <p class="fine">${esc(t.autor)}</p>
    <nav class="toc">${t.sections.map(s => `<a href="#/text/${id}/${s.id}" class="${s.id === sec.id ? "on" : ""}">${esc(s.titel)}</a>`).join("")}</nav>
    <div class="panel readable"><h3>${esc(sec.titel)}</h3><p>${esc(sec.blurb)}</p></div>
    ${(sec.plates || []).length ? `<div class="grid g4 secplates">${sec.plates.map(plateOf).filter(Boolean).map(plateFig).join("")}</div>` : ""}
    ${sec.viz ? `<div class="viz" id="viz"><p class="fine">Wird geladen…</p></div>` : ""}
    ${bilingual ? `<div class="langbar" id="langbar">
      ${[["both", `${origName} + Übersetzung`], ["orig", origName], ["en", "Übersetzung"]].map(([k, l]) =>
        `<button data-l="${k}" class="${k === lang ? "on" : ""}">${l}</button>`).join("")}</div>` : ""}
    <div id="units"></div>
    <div class="panel readable hinweis"><span class="tag">Quelle und Editionsnotiz</span>
      <p><b>Quelle.</b> ${esc(t.quelle)}</p><p>${esc(t.hinweis)}</p></div>`;
  bindPlates(view);
  if (sec.viz) fetch(`assets/viz/${sec.viz}.svg`).then(r => r.ok ? r.text() : "").then(svg => {
    const el = document.getElementById("viz");
    if (el) el.innerHTML = svg || "";
  });
  const box = view.querySelector("#units");
  for (const u of sec.units) {
    const showO = u.orig && lang !== "en", showE = !u.orig || lang !== "orig";
    const cls = ["unit", String(u.n) === unitN ? "hl" : ""].join(" ");
    box.insertAdjacentHTML("beforeend", `
      <div class="${cls}" id="u${u.n}">
        <div class="num"><a href="#/text/${id}/${sec.id}/${u.n}" title="Zitieren als ${esc(sec.zk)} [${u.n}]">[${u.n}]</a>
          ${u.pg ? `<span class="pg" title="${esc(t.pg_label || "")} page.line">${esc(t.pg_label || "")} ${esc(u.pg)}</span>` : ""}</div>
        <div>${u.titel ? `<h4>${esc(u.titel)}${u.lang && langs.length > 1 ? ` <span class="fine">(${esc(LANGS[u.lang] || u.lang)})</span>` : ""}</h4>` : ""}
          <div class="cols ${showO && showE ? "" : "one"}">
            ${showO ? `<div class="origcol"><div class="orig" lang="${esc(u.lang || t.orig_sprache)}"${t.rtl ? ' dir="rtl"' : ""}>${esc(u.orig)}</div>${u.tr ? `<div class="translit">${esc(u.tr)}</div>` : ""}</div>` : ""}
            ${showE ? `<div class="text">${esc(u.en)}</div>` : ""}
          </div></div>
        ${u.note ? `<div class="note">${esc(u.note)}</div>` : ""}
      </div>`);
  }
  view.querySelectorAll("#langbar button").forEach(b => b.onclick = () => {
    langPref = b.dataset.l;
    try { localStorage.setItem("klara_lang", langPref); } catch (e) { /* storage blocked */ }
    route();
  });
  if (unitN) { const el = document.getElementById("u" + unitN); if (el) el.scrollIntoView({ block: "center" }); }
}

/* ------------------------------------------------------------ compare */
async function compare([pid]) {
  const CMP = D.compare;
  const pair = (CMP.pairs || []).find(p => p.id === pid);
  if (!pair) {
    view.innerHTML = `
      <span class="tag">Vergleich</span><h1>Äbtissin, Rat und Reformatoren</h1>
      <p class="lede">${esc(CMP.lede)}</p>
      <div class="grid g2">${(CMP.pairs || []).map(p => `<a class="card" href="#/compare/${p.id}">
        <div>${p.voices.map(v => side((D.mods.shipped.find(m => m.id === v.text) || {}).side)).join(" ")}</div>
        <h3>${esc(p.titel)}</h3><p class="fine">${esc(p.frage)}</p></a>`).join("")}</div>`;
    return;
  }
  view.innerHTML = `<p class="fine"><a href="#/compare">← Alle Vergleiche</a></p><p class="fine">Wird geladen…</p>`;
  const docs = await Promise.all(pair.voices.map(v => {
    const m = D.mods.shipped.find(x => x.id === v.text);
    return text(m.datei).then(t => ({ v, m, t }));
  }));
  const col = ({ v, m, t }) => {
    const sec = t.sections.find(s => s.id === v.sec);
    const units = v.n.map(n => sec.units.find(u => u.n === n)).filter(Boolean);
    return `<div class="voice">
      <div class="vhead">${side(m.side)} <b>${esc(sec.autor || t.autor)}</b><br><span class="fine">${esc(t.jahr)} · ${esc(sec.titel)}</span></div>
      ${units.map(u => `<div class="vunit">
        <div class="fine"><a href="#/text/${m.id}/${sec.id}/${u.n}">${esc(sec.zk)} [${u.n}]</a>${u.titel ? ` · ${esc(u.titel)}` : ""}</div>
        <div class="text">${esc(u.en)}</div></div>`).join("")}
    </div>`;
  };
  view.innerHTML = `
    <p class="fine"><a href="#/compare">← Alle Vergleiche</a></p>
    <span class="tag">Vergleich</span><h1>${esc(pair.titel)}</h1>
    <p class="lede">${esc(pair.frage)}</p>
    <div class="panel readable"><p>${esc(pair.note)}</p></div>
    <div class="cmp n${docs.length}">${docs.map(col).join("")}</div>`;
}

/* ------------------------------------------------------------ timeline */
function timeline() {
  const T = D.timeline;
  view.innerHTML = `
    <span class="tag">Zeitleiste</span><h1>1467–1596</h1>
    <p class="lede">${esc(T.lede)}</p>
    <div class="legend">${Object.keys(SIDES).map(side).join(" ")}</div>
    <div class="tl">${T.stations.map(s => {
      const p = s.plate && plateOf(s.plate);
      return `<div class="st" style="--c:var(--${s.side})">
        <div><div class="d">${esc(s.d)} · ${side(s.side)}</div><h3>${esc(s.titel)}</h3><p>${esc(s.text)}</p>
        ${s.cite ? `<p class="fine"><a href="${s.cite}">✦ ${esc(s.citeLabel)}</a></p>` : ""}</div>
        ${p ? `<img src="assets/plates/${p.id}_t.jpg" alt="${esc(p.titel)}" title="${esc(p.titel)}">` : "<span></span>"}
      </div>`;
    }).join("")}</div>`;
}

/* ------------------------------------------------------------ plates */
function plates() {
  view.innerHTML = `
    <span class="tag">Tafeln</span><h1>Bildnisse, Ansichten, Drucke</h1>
    <p class="lede">${esc(D.plates.lede || "")}</p>
    <div class="grid g4">${D.plates.plates.map(plateFig).join("")}</div>
    <p class="fine">${esc(D.plates.credit)}</p>`;
  bindPlates(view);
}

function plateFig(p) {
  return `<figure class="plate card"><a href="#" data-p="${p.id}"><img src="assets/plates/${p.id}_t.jpg" alt="${esc(p.titel)}"></a>
      <figcaption>${side(p.side)} <b>${esc(p.titel)}</b><br>${esc(p.caption)}<br><i>${esc(p.source)}</i></figcaption></figure>`;
}

function bindPlates(root) {
  root.querySelectorAll("[data-p]").forEach(a => a.onclick = e => {
    e.preventDefault();
    const p = plateOf(a.dataset.p);
    const lb = document.createElement("div");
    lb.className = "lightbox";
    lb.innerHTML = `<figure><img src="assets/plates/${p.id}.jpg" alt="${esc(p.titel)}"><figcaption class="cap"><b>${esc(p.titel)}.</b> ${esc(p.caption)}</figcaption></figure>`;
    lb.onclick = () => lb.remove();
    document.body.append(lb);
  });
}

/* ------------------------------------------------------------ sources */
function sources() {
  view.innerHTML = `
    <span class="tag">Quellen, Methode, Grenzen</span><h1>Wie dieser Apparat gemacht ist</h1>
    <div class="readable">
    <p><b>Nur Gemeinfreies.</b> Jeder Text stammt aus einem Druck, dessen Schutzfrist abgelaufen ist; die Quelle steht auf seiner Seite. Moderne Editionen und Übersetzungen, die noch geschützt sind, werden nicht benutzt.</p>
    <p><b>Die Seite ist maßgeblich.</b> Die Hauptquelle sind Caritas Pirckheimers Denkwürdigkeiten in der Ausgabe von Constantin Höfler (Bamberg 1852), dazu Münchs Ausgabe ihres Nachlasses (1826) und die Drucke der Humanisten. Die maschinelle Texterkennung der Scans ist nur Hilfsmittel: Jede Stelle ist am Seitenbild gelesen, und jede Korrektur, die über das Offensichtliche hinausgeht, steht in den Anmerkungen. Die Schreibung des Herausgebers bleibt erhalten; seine erklärenden Zusätze in Klammern werden gekennzeichnet oder weggelassen.</p>
    <p><b>Arbeitsübersetzungen.</b> Die neuhochdeutschen Übersetzungen sind eigene Arbeit, nah am Original und gemeinfrei (CC0). Sie sind eine Lesehilfe, keine kritische Übersetzung; wo ein Wort unsicher ist, sagt es die Anmerkung.</p>
    <p><b>Stimmen und Abstände.</b> Die Denkwürdigkeiten sind der Bericht einer Partei, geschrieben von der Äbtissin für ihr Kloster. Die Gegenseite spricht in ihnen nur, wo Caritas sie zitiert, und in den Briefen, die sie abschrieb. Jedes Modul nennt, wer schrieb, wann und für wen; wo die Gegenseite eigene Texte hat, kommen sie zu Wort.</p>
    <p><b>Daten.</b> Die Daten der Texte stehen wie geschrieben (Heiligentage, Wochentage) mit dem heutigen Datum daneben.</p>
    </div>
    <h2>Abgedruckte Quellen</h2>
    ${D.mods.shipped.length ? `<div class="grid g2">${D.mods.shipped.map(m => `<div class="panel"><b>${esc(m.kurz)}</b><p class="fine" id="src-${m.id}">…</p></div>`).join("")}</div>` : `<p class="fine">Noch keine; die geplanten Module nennen ihre Quellen auf der Seite „Texte“.</p>`}
    ${(D.plates.plates || []).length ? `<h2>Tafeln</h2><p class="fine readable">${esc(D.plates.credit)}</p>` : ""}`;
  D.mods.shipped.forEach(async m => {
    const t = await text(m.datei);
    const el = document.getElementById("src-" + m.id);
    if (el) el.textContent = t.quelle;
  });
}

boot().catch(e => { view.innerHTML = `<p>Der Apparat konnte nicht geladen werden: ${esc(e.message)}</p>`; });
