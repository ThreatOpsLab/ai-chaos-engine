(function () {
  'use strict';

  // ---- Mock Data ----
  /** @type {{id:string, name:string, model:string, online:boolean, caps:string[]}[]} */
  const agents = [
    { id: 'agt-research', name: 'Researcher', model: 'gpt-4o-mini', online: true, caps: ['search', 'files'] },
    { id: 'agt-coder', name: 'Coder', model: 'claude-3.7-sonnet', online: true, caps: ['code', 'files'] },
    { id: 'agt-planner', name: 'Planner', model: 'gpt-4.1', online: false, caps: ['calendar'] },
  ];

  /** @type {{id:string, title:string, participants:string[], created:number, starred:boolean, tags:string[], messages:{id:string, author:string, role:'user'|'agent', content:string, ts:number, tools?:string[]}[]}[]} */
  const conversations = [
    {
      id: 'c1',
      title: 'Onboarding Improvements Q3',
      participants: ['agt-research', 'agt-coder'],
      created: Date.now() - 1000 * 60 * 60 * 24 * 5,
      starred: true,
      tags: ['product', 'onboarding'],
      messages: [
        { id: 'm1', author: 'You', role: 'user', content: 'Gather insights on onboarding drop-offs. Focus on mobile.', ts: Date.now() - 1000 * 60 * 60 * 24 * 5 + 1000 },
        { id: 'm2', author: 'Researcher', role: 'agent', content: 'Found 3 key pain points from last quarter. Also gathered 12 user interviews.', ts: Date.now() - 1000 * 60 * 60 * 24 * 5 + 3000, tools: ['Search'] },
        { id: 'm3', author: 'Coder', role: 'agent', content: 'Prototyped an experiment variant. Can ship behind a flag.', ts: Date.now() - 1000 * 60 * 60 * 24 * 5 + 6000 }
      ]
    },
    {
      id: 'c2',
      title: 'Weekly Planning — Marketing',
      participants: ['agt-planner', 'agt-research'],
      created: Date.now() - 1000 * 60 * 60 * 24 * 2,
      starred: false,
      tags: ['planning'],
      messages: [
        { id: 'm1', author: 'You', role: 'user', content: 'Draft plan for next week social campaigns. Include calendar integration.', ts: Date.now() - 1000 * 60 * 60 * 24 * 2 + 1200 },
        { id: 'm2', author: 'Planner', role: 'agent', content: 'Created a tentative schedule. Need access to calendar.', ts: Date.now() - 1000 * 60 * 60 * 24 * 2 + 2600, tools: ['Calendar'] }
      ]
    },
    {
      id: 'c3',
      title: 'Debugging flaky e2e tests',
      participants: ['agt-coder'],
      created: Date.now() - 1000 * 60 * 60 * 18,
      starred: false,
      tags: ['engineering', 'tests'],
      messages: [
        { id: 'm1', author: 'You', role: 'user', content: 'Why are our e2e tests flaky on CI only?', ts: Date.now() - 1000 * 60 * 60 * 18 + 1000 },
        { id: 'm2', author: 'Coder', role: 'agent', content: 'Likely due to resource contention. Try disabling parallelism for the failing group.', ts: Date.now() - 1000 * 60 * 60 * 18 + 3200 }
      ]
    }
  ];

  let currentConversationId = conversations[0]?.id || null;

  // ---- Helpers ----
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  function formatTime(ts) {
    const d = new Date(ts);
    return d.toLocaleString();
  }

  function createEl(tag, cls, text) {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (text) el.textContent = text;
    return el;
  }

  function initials(name) {
    return name.split(/\s+/).map(w => w[0]).slice(0,2).join('').toUpperCase();
  }

  function getAgent(agentId) {
    return agents.find(a => a.id === agentId);
  }

  function getConversation(convId) {
    return conversations.find(c => c.id === convId);
  }

  function highlight(text, q) {
    if (!q) return text;
    const esc = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return text.replace(new RegExp(`(${esc})`, 'ig'), '<mark class="highlight">$1</mark>');
  }

  // ---- Renderers ----
  function renderAgents() {
    const ul = $('#agentList');
    ul.innerHTML = '';
    for (const ag of agents) {
      const li = createEl('li');

      const meta = createEl('div', 'agent-meta');
      const av = createEl('div', 'avatar', initials(ag.name));
      const name = createEl('div');
      name.innerHTML = `<div class="agent-name">${ag.name}</div><div class="conversation-meta">${ag.model}</div>`;
      meta.append(av, name);

      const status = createEl('span', `badge ${ag.online ? 'online' : 'offline'}`, ag.online ? 'online' : 'offline');
      li.append(meta, status);

      ul.append(li);
    }
  }

  function renderConversations(filterText = '') {
    const ul = $('#conversationList');
    ul.innerHTML = '';
    const q = filterText.trim().toLowerCase();

    const filtered = conversations
      .map(c => ({
        conv: c,
        score: q ? ([c.title, ...c.tags, ...c.messages.map(m => m.content)].join(' ').toLowerCase().includes(q) ? 1 : 0) : 1
      }))
      .filter(x => x.score > 0)
      .sort((a, b) => (b.conv.starred - a.conv.starred) || (b.conv.created - a.conv.created));

    for (const { conv } of filtered) {
      const li = createEl('li');
      li.dataset.id = conv.id;

      const wrap = createEl('div', 'agent-meta');
      const av = createEl('div', 'avatar', '🗨️');
      const info = createEl('div');
      info.innerHTML = `<div class="conversation-title">${conv.title}</div>
        <div class="conversation-meta">${formatTime(conv.created)} · ${conv.tags.join(', ') || '—'}</div>`;
      wrap.append(av, info);

      const star = createEl('span', `star ${conv.starred ? 'active' : ''}`);
      star.textContent = conv.starred ? '★' : '☆';
      star.title = conv.starred ? 'Unstar' : 'Star';
      star.addEventListener('click', (e) => {
        e.stopPropagation();
        conv.starred = !conv.starred;
        renderConversations($('#historySearch').value);
      });

      li.append(wrap, star);
      li.addEventListener('click', () => {
        currentConversationId = conv.id;
        renderChat();
        highlightConversation(conv.id);
      });

      ul.append(li);
    }

    highlightConversation(currentConversationId);
  }

  function highlightConversation(convId) {
    $$('#conversationList li').forEach(li => {
      li.style.borderColor = (li.dataset.id === convId) ? 'var(--primary)' : 'transparent';
      li.style.background = (li.dataset.id === convId) ? 'rgba(0,163,255,0.10)' : 'rgba(255,255,255,0.02)';
    });
  }

  function renderChat() {
    const conv = getConversation(currentConversationId);
    const thread = $('#thread');
    thread.innerHTML = '';

    if (!conv) {
      $('#chatTitle').textContent = 'Welcome';
      $('#chatParticipants').innerHTML = '';
      thread.append(createEl('div', 'conversation-meta', 'Select or create a conversation.'));
      return;
    }

    $('#chatTitle').textContent = conv.title;

    // Participants chips
    const parts = conv.participants.map(pid => {
      const ag = getAgent(pid);
      return `<span class="pill">${ag ? ag.name : pid}</span>`;
    }).join('');
    $('#chatParticipants').innerHTML = parts;

    // Inspector metadata
    $('#conversationTags').innerHTML = conv.tags.map(t => `<span class="pill">#${t}</span>`).join('');
    $('#convCreated').textContent = formatTime(conv.created);
    const tokenCount = conv.messages.reduce((n, m) => n + Math.ceil(m.content.length / 4), 0);
    $('#convTokens').textContent = `${tokenCount.toLocaleString()} est.`;

    const q = $('#chatSearch').value.trim();

    for (const m of conv.messages) {
      const row = createEl('div', 'message');
      const av = createEl('div', 'avatar', m.role === 'user' ? 'YOU' : initials(m.author));

      const bubble = createEl('div', 'bubble');
      const meta = createEl('div', 'meta');
      meta.innerHTML = `<strong>${m.author}</strong><span>${formatTime(m.ts)}</span>`;
      const content = createEl('div', 'content');
      content.innerHTML = highlight(m.content, q);
      bubble.append(meta, content);

      if (m.tools?.length) {
        const tools = createEl('div', 'tools');
        tools.textContent = `Tools: ${m.tools.join(', ')}`;
        bubble.append(tools);
      }

      row.append(av, bubble);
      thread.append(row);
    }

    thread.scrollTop = thread.scrollHeight;
  }

  function renderRouteSelect() {
    const sel = $('#routeAgent');
    sel.innerHTML = agents.map(a => `<option value="${a.id}" ${a.online ? '' : 'disabled'}>${a.name} ${a.online ? '' : '(offline)'}</option>`).join('');
  }

  // ---- Actions ----
  function openConnectAgent() {
    $('#modalBackdrop').classList.remove('hidden');
    const d = /** @type {HTMLDialogElement} */ (document.getElementById('connectAgentModal'));
    if (!d.open) d.showModal();
    $('#agentNameInput').focus();
  }

  function closeConnectAgent() {
    $('#modalBackdrop').classList.add('hidden');
    const d = /** @type {HTMLDialogElement} */ (document.getElementById('connectAgentModal'));
    if (d.open) d.close();
  }

  function saveAgentFromModal() {
    const name = /** @type {HTMLInputElement} */(document.getElementById('agentNameInput')).value.trim();
    const model = /** @type {HTMLSelectElement} */(document.getElementById('agentModelInput')).value;
    const caps = Array.from(document.querySelectorAll('#connectAgentForm input[type="checkbox"]:checked')).map(cb => cb.value);
    if (!name) return;
    const id = `agt-${name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`;
    agents.push({ id, name, model, online: true, caps });
    renderAgents();
    renderRouteSelect();
    closeConnectAgent();
  }

  function newConversation() {
    const title = `Untitled ${new Date().toLocaleTimeString()}`;
    const id = `c${(Math.random()*1e6|0).toString(36)}`;
    const firstAgent = agents.find(a => a.online)?.id || agents[0]?.id;
    conversations.unshift({
      id,
      title,
      participants: firstAgent ? [firstAgent] : [],
      created: Date.now(),
      starred: false,
      tags: [],
      messages: []
    });
    currentConversationId = id;
    renderConversations($('#historySearch').value);
    renderChat();
  }

  function sendMessage() {
    const input = /** @type {HTMLTextAreaElement} */($('#composerInput'));
    const text = input.value.trim();
    if (!text) return;
    const conv = getConversation(currentConversationId);
    if (!conv) return;

    conv.messages.push({ id: `m${Date.now()}`, author: 'You', role: 'user', content: text, ts: Date.now() });
    input.value = '';
    renderChat();

    // Simulated agent reply
    const route = /** @type {HTMLSelectElement} */($('#routeAgent')).value;
    const agent = getAgent(route) || getAgent(conv.participants[0]);
    setTimeout(() => {
      conv.messages.push({
        id: `m${Date.now()}`,
        author: agent ? agent.name : 'Agent',
        role: 'agent',
        content: `Echo: ${text}`,
        ts: Date.now(),
        tools: agent?.caps?.slice(0, 1)
      });
      if (agent && !conv.participants.includes(agent.id)) conv.participants.push(agent.id);
      renderChat();
      renderConversations($('#historySearch').value);
    }, 500);
  }

  function summarizeConversation() {
    const conv = getConversation(currentConversationId);
    if (!conv) return;
    const summary = conv.messages.slice(-5).map(m => `${m.author}: ${m.content}`).join('\n');
    alert(`Mock Summary (last 5):\n\n${summary}`);
  }

  function exportConversation() {
    const conv = getConversation(currentConversationId);
    if (!conv) return;
    const blob = new Blob([JSON.stringify(conv, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${conv.title.replace(/[^a-z0-9]+/gi, '-').replace(/-+/g,'-')}.json`;
    a.click();
  }

  function deleteConversation() {
    const idx = conversations.findIndex(c => c.id === currentConversationId);
    if (idx >= 0) {
      const ok = confirm('Delete this conversation?');
      if (!ok) return;
      conversations.splice(idx, 1);
      currentConversationId = conversations[0]?.id || null;
      renderConversations($('#historySearch').value);
      renderChat();
    }
  }

  function toggleTheme() {
    const root = document.documentElement;
    const isLight = root.classList.toggle('light');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
  }

  function initTheme() {
    const saved = localStorage.getItem('theme');
    if (saved === 'light') document.documentElement.classList.add('light');
  }

  // ---- Command Palette ----
  const paletteCommands = [
    { id: 'new-chat', title: 'New Chat', action: newConversation },
    { id: 'summarize', title: 'Summarize Current Chat', action: summarizeConversation },
    { id: 'export', title: 'Export Current Chat', action: exportConversation },
    { id: 'connect-agent', title: 'Connect Agent…', action: openConnectAgent },
    { id: 'toggle-theme', title: 'Toggle Theme', action: toggleTheme },
  ];

  function openPalette() {
    const d = /** @type {HTMLDialogElement} */ (document.getElementById('commandPalette'));
    if (!d.open) d.showModal();
    $('#paletteInput').value = '';
    renderPaletteResults('');
    setTimeout(() => $('#paletteInput').focus(), 0);
  }

  function closePalette() {
    const d = /** @type {HTMLDialogElement} */ (document.getElementById('commandPalette'));
    if (d.open) d.close();
  }

  function renderPaletteResults(q) {
    const ul = $('#paletteResults');
    const k = q.trim().toLowerCase();
    const items = paletteCommands.filter(c => c.title.toLowerCase().includes(k));
    ul.innerHTML = items.map(c => `<li data-id="${c.id}">${c.title}</li>`).join('');
  }

  // ---- Event Wiring ----
  function wireEvents() {
    $('#connectAgentBtn').addEventListener('click', openConnectAgent);
    $('#closeConnectModal').addEventListener('click', closeConnectAgent);
    $('#saveAgentBtn').addEventListener('click', (e) => { e.preventDefault(); saveAgentFromModal(); });

    $('#newChatBtn').addEventListener('click', newConversation);

    $('#historySearch').addEventListener('input', (e) => {
      const q = /** @type {HTMLInputElement} */(e.target).value;
      renderConversations(q);
    });

    $('#chatSearch').addEventListener('input', renderChat);

    $('#sendBtn').addEventListener('click', sendMessage);
    $('#composerInput').addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'enter') {
        e.preventDefault();
        sendMessage();
      }
      if (e.key === '/' && !e.shiftKey && !e.altKey && !e.ctrlKey && !e.metaKey) {
        // show simple command hint (mock)
      }
    });

    $('#summarizeBtn').addEventListener('click', summarizeConversation);
    $('#exportBtn').addEventListener('click', exportConversation);
    $('#deleteBtn').addEventListener('click', deleteConversation);
    $('#themeToggle').addEventListener('click', toggleTheme);

    // Palette
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openPalette();
      } else if (e.key === 'Escape') {
        closePalette();
      }
    });

    $('#commandPaletteBtn').addEventListener('click', openPalette);
    $('#paletteInput').addEventListener('input', (e) => {
      renderPaletteResults(/** @type {HTMLInputElement} */(e.target).value);
    });
    $('#paletteResults').addEventListener('click', (e) => {
      const li = /** @type {HTMLElement} */(e.target.closest('li'));
      if (!li) return;
      const cmd = paletteCommands.find(c => c.id === li.dataset.id);
      closePalette();
      cmd?.action();
    });
  }

  // ---- Init ----
  function init() {
    initTheme();
    renderAgents();
    renderConversations();
    renderRouteSelect();
    renderChat();
    wireEvents();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();