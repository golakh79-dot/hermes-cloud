import { connect } from "cloudflare:sockets";

const userID = '3ba4a4af-e35d-4220-a287-be91edd0090d';
const WS_READY_STATE_OPEN = 1;

function uuidToBytes(uuid) {
  const hex = uuid.replaceAll("-", "").toLowerCase();
  if (!/^[0-9a-f]{32}$/.test(hex)) {
    throw new Error("Invalid UUID");
  }
  const bytes = new Uint8Array(16);
  for (let i = 0; i < 16; i++) {
    bytes[i] = parseInt(hex.slice(i * 2, i * 2 + 2), 16);
  }
  return bytes;
}

function secureEqual(a, b) {
  if (a.length !== b.length) return false;
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a[i] ^ b[i];
  }
  return result === 0;
}

function concatBytes(a, b) {
  const result = new Uint8Array(a.length + b.length);
  result.set(a, 0);
  result.set(b, a.length);
  return result;
}

async function toUint8Array(data) {
  if (data instanceof ArrayBuffer) {
    return new Uint8Array(data);
  }
  if (ArrayBuffer.isView(data)) {
    return new Uint8Array(data.buffer, data.byteOffset, data.byteLength);
  }
  if (typeof Blob !== "undefined" && data instanceof Blob) {
    return new Uint8Array(await data.arrayBuffer());
  }
  throw new Error("Binary WebSocket frame required");
}

function parseVlessHeader(buffer, expectedUuid) {
  let i = 0;
  const need = (length) => buffer.length >= i + length;
  
  if (!need(18)) {
    return { incomplete: true };
  }
  
  const version = buffer[i++];
  const userId = buffer.slice(i, i + 16);
  i += 16;
  
  if (!secureEqual(userId, expectedUuid)) {
    return { incomplete: false, error: "Authentication failed" };
  }
  
  const optionLength = buffer[i++];
  i += optionLength;
  
  if (!need(1)) {
    return { incomplete: true };
  }
  const command = buffer[i++];
  
  if (!need(2)) {
    return { incomplete: true };
  }
  const port = (buffer[i] << 8) | buffer[i + 1];
  i += 2;
  
  if (!need(1)) {
    return { incomplete: true };
  }
  const addressType = buffer[i++];
  
  let hostname = "";
  
  if (addressType === 1) {
    if (!need(4)) return { incomplete: true };
    hostname = `${buffer[i]}.${buffer[i+1]}.${buffer[i+2]}.${buffer[i+3]}`;
    i += 4;
  } else if (addressType === 2) {
    if (!need(1)) return { incomplete: true };
    const length = buffer[i++];
    if (!need(length)) return { incomplete: true };
    hostname = new TextDecoder().decode(buffer.slice(i, i + length));
    i += length;
  } else if (addressType === 3) {
    if (!need(16)) return { incomplete: true };
    const parts = [];
    for (let n = 0; n < 8; n++) {
      const value = (buffer[i + n * 2] << 8) | buffer[i + n * 2 + 1];
      parts.push(value.toString(16));
    }
    hostname = parts.join(":");
    i += 16;
  } else {
    return { incomplete: false, error: "Unsupported address type" };
  }
  
  return {
    incomplete: false,
    version,
    command,
    port,
    hostname,
    payload: buffer.slice(i),
  };
}

async function pumpTcpToWebSocket(socket, ws) {
  const reader = socket.readable.getReader();
  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      if (ws.readyState !== WS_READY_STATE_OPEN) break;
      if (value && value.byteLength > 0) {
        ws.send(value);
      }
    }
  } finally {
    try { reader.releaseLock(); } catch {}
  }
}

async function handleVless(ws, expectedUuid) {
  let pending = new Uint8Array(0);
  let socket = null;
  let writer = null;
  let connected = false;
  let closed = false;
  
  let chain = Promise.resolve();
  
  function closeTcpOnly() {
    try { writer?.releaseLock(); } catch {}
    try { socket?.close(); } catch {}
  }
  
  function shutdown(code = 1000, reason = "") {
    if (closed) return;
    closed = true;
    closeTcpOnly();
    try {
      if (ws.readyState === WS_READY_STATE_OPEN) {
        ws.close(code, reason);
      }
    } catch {}
  }
  
  ws.addEventListener("close", () => {
    shutdown(1000, "WebSocket closed");
  });
  
  ws.addEventListener("error", (event) => {
    console.error("WebSocket error", event);
    shutdown(1011, "WebSocket error");
  });
  
  ws.addEventListener("message", (event) => {
    chain = chain
      .then(async () => {
        if (closed) return;
        const data = await toUint8Array(event.data);
        
        if (connected) {
          await writer.write(data);
          return;
        }
        
        pending = concatBytes(pending, data);
        const parsed = parseVlessHeader(pending, expectedUuid);
        
        if (parsed.incomplete) {
          return;
        }
        
        if (parsed.error) {
          console.error("VLESS header parse failed:", parsed.error);
          shutdown(1011, "VLESS error");
          return;
        }
        
        if (parsed.command !== 1) {
          console.error("Unsupported command:", parsed.command);
          shutdown(1011, "Unsupported command");
          return;
        }
        
        console.log(`Connecting TCP to ${parsed.hostname}:${parsed.port}`);
        
        try {
          socket = connect({ hostname: parsed.hostname, port: parsed.port });
          await socket.opened;
        } catch (e) {
          console.error("TCP connect failed:", e);
          shutdown(1011, "TCP connect failed");
          return;
        }
        
        writer = socket.writable.getWriter();
        connected = true;
        
        ws.send(new Uint8Array([parsed.version, 0]));
        
        if (parsed.payload.length > 0) {
          await writer.write(parsed.payload);
        }
        
        pending = new Uint8Array(0);
        
        pumpTcpToWebSocket(socket, ws)
          .then(() => shutdown(1000, "TCP closed"))
          .catch((error) => {
            console.error("TCP read error:", error);
            shutdown(1011, "TCP error");
          });
      })
      .catch((error) => {
        console.error("VLESS proxy error:", error);
        shutdown(1011, "Proxy error");
      });
  });
}

export default {
  async fetch(request, env) {
    try {
      const url = new URL(request.url);
      const path = env.VLESS_PATH || "/ws";
      
      if (url.pathname !== path) {
        return new Response("Not found", {
          status: 404,
          headers: { "Cache-Control": "no-store" },
        });
      }
      
      if (request.headers.get("Upgrade")?.toLowerCase() !== "websocket") {
        return new Response("WebSocket required", {
          status: 426,
          headers: { "Cache-Control": "no-store" },
        });
      }
      
      const uuid = env.VLESS_UUID || userID;
      let expectedUuid;
      try {
        expectedUuid = uuidToBytes(uuid);
      } catch (error) {
        console.error("Invalid VLESS_UUID configuration", error);
        return new Response("Server configuration error", { status: 500 });
      }
      
      const pair = new WebSocketPair();
      const [client, server] = Object.values(pair);
      
      server.accept();
      
      const earlyDataHeader = request.headers.get("sec-websocket-protocol") || "";
      const earlyData = earlyDataHeader ? await toUint8Array(earlyDataHeader) : null;
      
      if (earlyData && earlyData.length > 0) {
        server.send(earlyData);
      }
      
      handleVless(server, expectedUuid).catch((error) => {
        console.error("Unhandled VLESS error:", error);
      });
      
      return new Response(null, {
        status: 101,
        webSocket: client,
      });
    } catch (err) {
      console.error("Fetch error:", err);
      return new Response(`Error: ${err.message}\nStack: ${err.stack}`, { status: 500 });
    }
  },
};