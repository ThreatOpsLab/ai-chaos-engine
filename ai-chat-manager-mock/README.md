# AI Chat Manager — Mock UI

A static, self-contained mock of an AI Chat Manager with multi-agent routing and searchable chat history. No build step required.

## Run
- Open `index.html` in your browser, or use a simple local server:
  - Python: `python3 -m http.server 8080` and visit `http://localhost:8080/ai-chat-manager-mock/`

## Features (Mocked)
- Multiple agents list with online/offline status
- Conversation history with search and pinning
- In-chat search with highlight
- Message composer with routing selector and simulated agent replies
- Connect Agent modal to add mock agents
- Right-side inspector with conversation metadata
- Command palette (Ctrl/Cmd K): new chat, summarize, export, toggle theme
- Light/Dark theme toggle

## Notes
- Data is in-memory only (refresh resets state)
- Export downloads the current conversation as JSON (mock)