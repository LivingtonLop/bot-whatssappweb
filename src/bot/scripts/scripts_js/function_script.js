var chatContainer = document.querySelector(arguments[0]);

if (chatContainer){

    window.message;
    window.observer = new MutationObserver(function (mutations) {

        for (var mutation of mutations) {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === 1 && node.getAttribute("role") === "row") { // Asegurar que es un elemento HTML
        
                    try {
                        
                        window.message = node


                    } catch (error) {
                        console.error("Error al buscar los elementos: ", error);
                    }
                
                }
            });
        }    
    
    });

    observer.observe(chatContainer, { childList: true, subtree: true });    

    console.log("🔹 Monitoreo de palabras...");

}else{

    console.log("⚠️ No se encontró el contenedor del chat.");

}



var chatContainer = document.querySelector(arguments[0]);

if (chatContainer) {
    var mensajeCount = {}; // Guarda la cantidad de veces que aparece un mensaje
    var tiempoReset = arguments[2]; // x segundos para detectar spam
    var limiteSpam = arguments[3]; // Máximo x elementos multimedia en xs antes de activar spam
    var spamVisualCount = 0; // Contador de stickers, imágenes, GIFs, audios y videos
    
    window.spamDetected = false;
    window.observer = new MutationObserver(function (mutations) {
        var query_selector_media = this;

        for (var mutation of mutations) {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === 1) { // Asegurar que es un elemento HTML
                    
                    let multimediaElement = node.querySelectorAll(query_selector_media);
    
                    try {
                        
                        if (multimediaElement.length > 0) {

                            multimediaElement.forEach(element=>{
                                spamVisualCount++; // Si existe, aumenta el contador
                            });

                        }
                        // Detecta mensajes repetidos
                        
                        var texto = node.innerText?.trim();
                        if (texto) {
                            mensajeCount[texto] = (mensajeCount[texto] || 0) + 1;
                        }

                    } catch (error) {
                        console.error("Error al buscar los elementos multimedia: ", error);
                    }

                }
            });
        }

        // Si hay más de 10 elementos multimedia o mensajes repetidos
        var mensajesSpam = Object.values(mensajeCount).filter(count => count > 3).length; // Mensajes repetidos
        window.spamDetected = spamVisualCount > limiteSpam || mensajesSpam > 3;

        if (window.spamDetected) {
            console.log("⚠️ SPAM DETECTADO ⚠️");
            window.spamDetected = true;
            observer.disconnect(); // 🔴 DETIENE el observer
            console.log("⏸ Monitoreo detenido. Esperando reactivación...");
            
        }
    }.bind(arguments[1]));//Pasamos `miVariable` como `this`

    observer.observe(chatContainer, {childList: true, subtree: true});

    // Reinicia los contadores cada 5 segundos
    setInterval(() => {
        Object.keys(mensajeCount).forEach(key => delete mensajeCount[key]);
        spamVisualCount = 0;
    }, tiempoReset);
    

    console.log("🔹 Monitoreo de mensajes activado...");
} else {
    console.log("⚠️ No se encontró el contenedor del chat.");
}



// return window.spamDetected;



function obtenerYVaciarMensaje() {
    let message = window.message; // Guarda la referencia al nodo
    window.message = null; // Borra la referencia en window

    return message; // Devuelve el nodo
}

// return obtenerYVaciarMensaje();


    console.log("🔄 Reiniciando el observer...");
    window.spamDetected = false;

    window.observer.observe(document.querySelector(arguments[0]), {childList: true, subtree: true});



window.isObserverActive = false;
window.observerListMember = null;
window.listMemberResponse = false;

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
    } else {
        if (listMember){
            window.reconectarObserverListMember(listMember)    
        }
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

