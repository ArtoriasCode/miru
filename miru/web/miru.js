const listenedJSFunctions = {};
const pendingCalls = new Map();

let socket;
let callId = 0;
let socketReady = false;

export const MIRU_READY_EVENT = "MIRU_READY";

export function listen(name, fn) {
    listenedJSFunctions[name] = fn;
}

export function call_py(name, ...args) {
    return new Promise((resolve, reject) => {
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            return reject(new Error("Socket not ready"));
        }

        const id = ++callId;

        const timeout = setTimeout(() => {
            pendingCalls.delete(id);
            reject(new Error("Socket timeout"));
        }, 60000);

        pendingCalls.set(id, {
            resolve: (result) => {
                clearTimeout(timeout);
                resolve(result);
            },
            reject: (err) => {
                clearTimeout(timeout);
                reject(err);
            }
        });

        socket.send(JSON.stringify({
            type: "call",
            id,
            name,
            args
        }));
    });
}

export function setup() {
    setupWebSocket();
}

function setupWebSocket() {
    socket = new WebSocket(`ws://${location.host}/__miru_ws__`);

    socket.addEventListener("open", () => {
        socketReady = true;
        console.log("[Miru] WebSocket connected");
        dispatchMiruReady();
    });

    socket.addEventListener("message", (event) => {
        let msg;

        try {
            msg = JSON.parse(event.data);
        } catch {
            console.warn("[Miru] Invalid JSON:", event.data);
            return;
        }

        if (msg.type === "result") {
            pendingCalls.get(msg.id)?.resolve(msg.result);
            pendingCalls.delete(msg.id);
        } else if (msg.type === "error") {
            pendingCalls.get(msg.id)?.reject(new Error(msg.error));
            pendingCalls.delete(msg.id);
        } else if (msg.type === "call") {
            const fn = listenedJSFunctions[msg.name];

            if (fn) {
                try {
                    fn(...msg.args);
                } catch (e) {
                    console.error(`[Miru] JS error in "${msg.name}":`, e);
                }
            }
        }
    });

    socket.addEventListener("close", () => {
        console.warn("[Miru] WebSocket closed. Retrying...");
        setTimeout(setupWebSocket, 1000);
    });

    socket.addEventListener("error", (e) => {
        console.error("[Miru] WebSocket error:", e);
        socket.close();
    });
}

function dispatchMiruReady() {
    if (socketReady) {
        document.dispatchEvent(new CustomEvent(MIRU_READY_EVENT));
    }
}

export const miru = {
    call_py,
    listen,
    setup,
    MIRU_READY_EVENT
};
