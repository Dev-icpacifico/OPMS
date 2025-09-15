(function () {
  function $el(sel) { return document.querySelector(sel); }
  function el(name, cls) { const x = document.createElement(name); if (cls) x.className = cls; return x; }

  function appendMessage(container, { role, content, ts }) {
    const wrap = el("div", `message ${role === "user" ? "msg-user" : "msg-assistant"}`);
    const meta = el("div", "msg-meta");
    meta.textContent = (role === "user" ? "Tú" : "Agente") + (ts ? " · " + ts : "");
    wrap.appendChild(meta);
    const body = el("div", "msg-content");
    body.textContent = content || "";
    wrap.appendChild(body);
    container.appendChild(wrap);
    container.scrollTop = container.scrollHeight;
    return wrap;
  }

  function hydrateHistory(messagesEl, history) {
    messagesEl.innerHTML = "";
    (history.messages || []).forEach(m => {
      appendMessage(messagesEl, {
        role: m.role,
        content: m.content,
        ts: new Date(m.created_at).toLocaleString(),
      });
    });
  }

  function openSSE(streamUrl, assistantMsgEl) {
    const contentEl = assistantMsgEl.querySelector(".msg-content");
    const typing = document.createElement("span");
    typing.className = "msg-typing";
    typing.textContent = " escribiendo…";
    contentEl.appendChild(typing);

    const es = new EventSource(streamUrl);

    es.addEventListener("token", (e) => {
      const data = JSON.parse(e.data);
      typing.remove();
      contentEl.textContent += data.delta || "";
      assistantMsgEl.scrollIntoView({ behavior: "smooth", block: "end" });
    });

    es.addEventListener("final", (e) => {
      typing.remove?.();
      es.close();
      $el("#composer-input").focus();
    });

    es.addEventListener("error", (e) => {
      console.error("SSE error", e);
      es.close();
      const banner = document.createElement("div");
      banner.className = "banner error";
      banner.textContent = "⚠️ Error en el stream.";
      document.body.prepend(banner);
      setTimeout(() => banner.remove(), 4000);
    });
  }

  function boot(cfg) {
    const messagesEl = $el("#messages");
    const input = $el("#composer-input");

    // Historial (vacío en este MVP)
    fetch(cfg.historyUrl, { credentials: "include" })
      .then(r => r.json())
      .then(data => hydrateHistory(messagesEl, data))
      .catch(console.error);

    // Enter = enviar; Shift+Enter = nueva línea
    input.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter" && !ev.shiftKey) {
        ev.preventDefault();
        const text = input.value.trim();
        if (!text) return;

        const ts = new Date().toLocaleString();
        appendMessage(messagesEl, { role: "user", content: text, ts });

        const placeholder = appendMessage(messagesEl, { role: "assistant", content: "", ts });

        fetch(cfg.postUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-CSRFToken": cfg.csrfToken },
          credentials: "include",
          body: JSON.stringify({ message: text })
        })
        .then(r => r.json())
        .then(data => {
          input.value = "";
          if (data.status !== "accepted" || !data.stream_url) {
            throw new Error("Respuesta no válida");
          }
          openSSE(data.stream_url, placeholder);
        })
        .catch(err => {
          console.error(err);
          const banner = document.createElement("div");
          banner.className = "banner error";
          banner.textContent = "⚠️ No se pudo enviar el mensaje.";
          document.body.prepend(banner);
          setTimeout(() => banner.remove(), 4000);
        });
      }
    });
  }

  window.CHAT_BOOT = boot;
})();
