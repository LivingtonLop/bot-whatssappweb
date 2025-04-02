window.initObserver = function (chatSelector, querySelectorMedia, tiempoReset, limiteSpam) {
    var chatContainer = document.querySelector(chatSelector);
    
    if (!chatContainer) {
        console.log("⚠️ No se encontró el contenedor del chat.");
        return;
    }

    window.messageChat = null;
    window.spamDetected = false;
    var mensajeCount = {}; // Guarda la cantidad de veces que aparece un mensaje
    var spamVisualCount = 0;

    window.observer = new MutationObserver(function (mutations) {
        mutations.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === 1) {
                    try {
                        let multimediaElement = node.querySelectorAll(querySelectorMedia);
                        if (multimediaElement.length > 0) {
                            spamVisualCount += multimediaElement.length;
                        }

                        var texto = node.innerText?.trim();
                        if (texto) {
                            mensajeCount[texto] = (mensajeCount[texto] || 0) + 1;
                        }

                        window.messageChat = node;
                    } catch (error) {
                        console.error("Error al buscar elementos: ", error);
                    }
                }
            });
        });

        var mensajesSpam = Object.values(mensajeCount).filter(count => count > 3).length;
        window.spamDetected = spamVisualCount > limiteSpam || mensajesSpam > 3;

        if (window.spamDetected) {
            console.log("⚠️ SPAM DETECTADO ⚠️");
            window.observer.disconnect();
            console.log("⏸ Monitoreo detenido.");
        }
    });

    window.observer.observe(chatContainer, { childList: true, subtree: true });
    setInterval(() => {
        Object.keys(mensajeCount).forEach(key => delete mensajeCount[key]);
        spamVisualCount = 0;
    }, tiempoReset);

    console.log("🔹 Monitoreo activado...");
};

window.getSpamDetected = function () {
    return window.spamDetected;
};

window.obtenerYVaciarMensaje = function () {
    let message = window.messageChat;
    window.messageChat = null;
    return message;
};

window.reiniciarObserver = function (chatSelector) {
    console.log("🔄 Reiniciando el observer...");
    window.spamDetected = false;
    window.observer.observe(document.querySelector(chatSelector), { childList: true, subtree: true });
};


//busqueda de miembros
window.initObserverListMember = function (listMember) {
    if (!window.isObserverActive && listMember) {
        window.observerListMember = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                if (mutation.type === 'childList' || mutation.type === 'characterData') {
                    window.listMemberResponse = true;
                }
            });
        });
        const config = { childList: true, subtree: true, characterData: true };
        window.observerListMember.observe(listMember, config);
        window.isObserverActive = true;
        console.log("Observador iniciado");
    } else if (listMember) {
        window.reconectarObserverListMember(listMember);
    }
};

window.desconectarObserverListMember = function () {
    if (window.observerListMember) {
        window.observerListMember.disconnect();
        window.isObserverActive = false;
        console.log("Observador desconectado");
    }
};

window.reconectarObserverListMember = function (listMember) {
    if (window.observerListMember && listMember) {
        const config = { childList: true, subtree: true, characterData: true };
        window.observerListMember.observe(listMember, config);
        console.log("Observador reconectado");
    } else {
        console.log("No hay observador activo o listMember no proporcionado");
    }
};

window.flagListMember = function (listMember) {
    if (!window.isObserverActive) {
        window.initObserverListMember(listMember);
    } else {
        console.log("Si hay observador activo");
    }
};
