/* Section search uses a script index, so snippets also work with file://. */
"use strict";
const SectionSearch = (() => {
  const normalize = text => text.normalize("NFKC").toLowerCase().replace(/\s+/g, " ").trim();
  const tokens = query => [...new Set(normalize(query).match(/[\p{Letter}\p{Number}_]+/gu) || [])];

  function snippet(text, query) {
    const words = tokens(query);
    const lower = normalize(text);
    const positions = words.map(word => lower.indexOf(word)).filter(index => index >= 0);
    const at = positions.length ? Math.min(...positions) : 0;
    const start = Math.max(0, at - 65);
    const end = Math.min(text.length, start + 240);
    return (start ? '…' : '') + text.slice(start, end).trim() + (end < text.length ? '…' : '');
  }

  function search(entries, query) {
    const words = tokens(query);
    if (!words.length) return [];
    const phrase = normalize(query);
    return entries.flatMap(entry => {
      const title = normalize(entry.title);
      const text = normalize(entry.text);
      // Match the local section rather than every section sharing a page title.
      if (!words.every(word => title.includes(word) || text.includes(word))) return [];
      const score = (title.includes(phrase) ? 100 : 0) +
        (text.includes(phrase) ? 35 : 0) +
        words.reduce((sum, word) => sum + (title.includes(word) ? 15 : 3), 0);
      return [{...entry, score, snippet: snippet(entry.text || entry.title, query)}];
    }).sort((a, b) => b.score - a.score || a.url.localeCompare(b.url));
  }

  function highlight(element, text, query) {
    const words = tokens(query).sort((a, b) => b.length - a.length);
    if (!words.length) { element.textContent = text; return; }
    const escape = word => word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const pattern = new RegExp(words.map(escape).join('|'), 'giu');
    let end = 0;
    for (const match of text.matchAll(pattern)) {
      element.appendChild(document.createTextNode(text.slice(end, match.index)));
      const mark = document.createElement('mark');
      mark.textContent = match[0];
      element.appendChild(mark);
      end = match.index + match[0].length;
    }
    element.appendChild(document.createTextNode(text.slice(end)));
  }

  function render(root, results, query, limit) {
    root.replaceChildren();
    results.slice(0, limit).forEach(result => {
      const card = document.createElement('li');
      const path = document.createElement('p');
      path.className = 'section-search-path';
      path.textContent = result.path || result.page;
      card.appendChild(path);
      const heading = document.createElement('h2');
      const link = document.createElement('a');
      const [page, anchor] = result.url.split('#');
      link.href = page + '?highlight=' + encodeURIComponent(query) + (anchor ? '#' + anchor : '');
      highlight(link, result.title, query);
      heading.appendChild(link);
      card.appendChild(heading);
      const preview = document.createElement('p');
      preview.className = 'section-search-preview';
      highlight(preview, result.snippet, query);
      card.appendChild(preview);
      root.appendChild(card);
    });
  }

  function init() {
    const app = document.getElementById('section-search');
    if (!app) return;
    const zh = app.dataset.language.startsWith('zh');
    const query = (new URLSearchParams(window.location.search).get('q') || '').trim();
    app.querySelector('[name="q"]').value = query;
    const status = document.getElementById('section-search-status');
    if (!query) {
      status.textContent = zh ? '输入关键词，搜索文档全部章节。' : 'Enter keywords to search all sections.';
      return;
    }
    if (!window.SECTION_SEARCH_INDEX) {
      status.textContent = zh ? '搜索索引加载失败，请刷新页面。' : 'Search index failed to load. Please refresh.';
      return;
    }
    const results = search(window.SECTION_SEARCH_INDEX.entries, query);
    status.textContent = results.length
      ? (zh ? `找到 ${results.length} 个相关章节` : `Found ${results.length} matching sections`)
      : (zh ? '未找到相关内容，请尝试更短的关键词或接口名称。' : 'No matches. Try shorter keywords or an API name.');
    const root = document.getElementById('section-search-results');
    let limit = 20;
    render(root, results, query, limit);
    if (results.length > limit) {
      const more = document.createElement('button');
      more.className = 'section-search-more';
      more.textContent = zh ? '显示更多结果' : 'Show more results';
      more.addEventListener('click', () => {
        limit += 20;
        render(root, results, query, limit);
        if (limit >= results.length) more.remove();
      });
      app.appendChild(more);
    }
  }
  if (typeof document !== 'undefined') document.addEventListener('DOMContentLoaded', init);
  return {search, snippet, tokens, highlight, render};
})();
