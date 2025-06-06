document.addEventListener('DOMContentLoaded', function() {
    const clientListDiv = document.getElementById('client-list');
    const devicePageDiv = document.getElementById('device-page');
    const backToListButton = document.getElementById('back-to-list-button');
    const screenshotDisplay = document.getElementById('screenshot-display');
    const deviceNameHeader = document.getElementById('device-name-header');
    const commandInput = document.getElementById('command-input');
    const executeCommandButton = document.getElementById('execute-command-button');
    const PowerOffCommandButton = document.getElementById('PowerOff-command-button');
    const executeAPIbutton = document.getElementById('execute-api-button');
    const commandOutputDiv = document.getElementById('command-output');
    const connectedCountSpan = document.getElementById('connected-count');
    const disconnectedCountSpan = document.getElementById('disconnected-count');
    const apiInput = document.getElementById('api-input');
    // PDF report elements
    const checkPdfButton = document.getElementById('check-pdf-button');
    const generatePdfButton = document.getElementById('generate-pdf-button');
    const downloadPdfButton = document.getElementById('download-pdf-button');
    const pdfStatusDiv = document.getElementById('pdf-status');

    let currentClientId = null;
    let screenshotPollingInterval;
    let resourcePollingInterval;
    let logsPollingInterval;
    let scanResultsPollingInterval;
    let lastProcessedLogTime = null;
    let lastCommandIdSent = null;
    let pdfExists = false;
    
    // Fonction pour vérifier si l'OS est Windows
    function isWindows(osType) {
        return osType && osType.toLowerCase().includes('windows');
    }

    function fetchClients() {
        fetch('/clients')
            .then(response => response.json())
            .then(clients => {
                clientListDiv.innerHTML = '';
                let connectedClients = 0;
                let disconnectedClients = 0;

                clients.forEach(client => {
                    const clientBlock = document.createElement('div');
                    clientBlock.className = 'client-block';
                    
                    // Vérifier si c'est Windows et ajouter l'icône appropriée
                    // Utiliser le chemin correct vers windows.png
                    const osDisplay = isWindows(client.os_type) 
                        ? `<img src="windows.png" alt="Windows" class="os-icon" width="25" height="25"/> ${client.os_type}`
                        : client.os_type;
                    
                    clientBlock.innerHTML = `
                        <h3>${client.name}</h3>
                        <p>OS: ${osDisplay}</p>
                        <p>Connecté: ${client.is_connected ? 'Oui' : 'Non'}</p>
                        <button onclick="showDevicePage(${client.id}, '${client.name}')">Surveiller</button>
                        <button onclick="disconnectClient(${client.id})">Déconnecter</button>
                    `;
                    clientListDiv.appendChild(clientBlock);
                    if (client.is_connected) {
                        connectedClients++;
                    } else {
                        disconnectedClients++;
                    }
                    os_computer = client.os_type;
                });
                connectedCountSpan.textContent = connectedClients;
                disconnectedCountSpan.textContent = disconnectedClients;
            })
            .catch(error => console.error('Error fetching clients:', error));
    }

    window.showDevicePage = function(clientId, clientName) {
        currentClientId = clientId;
        deviceNameHeader.textContent = clientName;
        devicePageDiv.style.display = 'block';
        clientListDiv.style.display = 'none';
        fetchScreenshot(clientId);
        startScreenshotPolling(clientId);
        fetchResourceInfo(clientId);
        startResourcePolling(clientId);
        startLogsPolling(clientId);
        fetchScanResults(clientId);  // Fetch scan results
        startScanResultsPolling(clientId); // Start polling for scan results
        loadCommandHistory(clientId); // Charger l'historique des commandes
        lastProcessedLogTime = null;
        
        // Stockage de l'ID client dans le localStorage pour persistance
        localStorage.setItem('currentClientId', clientId);
        localStorage.setItem('currentClientName', clientName);
        
        // Activer les boutons de commande
        enableCommandButtons();

        // Fetch and apply client settings
        fetch(`/client/${clientId}/settings/admin`)
            .then(response => response.json())
            .then(settings => {
                applyFeatureVisibility(settings);
            })
            .catch(error => {
                console.error("Erreur lors de la récupération des paramètres:", error);
            });

        initializePdfSection(clientId);
    }

    // Fonction pour activer/désactiver les boutons de commande en fonction de la sélection d'appareil
    function enableCommandButtons() {
        const commandButtons = document.querySelectorAll('.command-buttons button');
        const executeCommandButton = document.getElementById('execute-command-button');
        
        if (currentClientId) {
            commandButtons.forEach(button => {
                button.disabled = false;
            });
            executeCommandButton.disabled = false;
        } else {
            commandButtons.forEach(button => {
                button.disabled = true;
            });
            executeCommandButton.disabled = true;
        }
    }
    
    window.disconnectClient = function(clientId) {
        fetch(`/client/${clientId}/disconnect`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            fetchClients();
        })
        .catch(error => console.error('Error disconnecting client:', error));
    }

    backToListButton.addEventListener('click', function() {
        devicePageDiv.style.display = 'none';
        clientListDiv.style.display = 'flex';
        stopScreenshotPolling();
        stopResourcePolling();
        stopLogsPolling();
        stopScanResultsPolling(); // Stop polling for scan results
        
        // Effacer les données stockées pour éviter toute restauration future
        localStorage.removeItem('currentClientId');
        localStorage.removeItem('currentClientName');
    });

    function fetchScreenshot(clientId) {
        screenshotDisplay.src = `/screenshots/client_${clientId}_latest.png?timestamp=${new Date().getTime()}`;
    }

    function startScreenshotPolling(clientId) {
        screenshotPollingInterval = setInterval(() => {
            fetchScreenshot(clientId);
        }, 5000);
    }

    function stopScreenshotPolling() {
        clearInterval(screenshotPollingInterval);
    }

    function generateCommandId() {
        return Date.now().toString() + Math.floor(Math.random() * 10000).toString();
    }

    // Fonction pour envoyer une commande en identifiant le bouton utilisé
    function sendCommandWithButton(clientId, command, buttonType) {
        if (!clientId) {
            return false;
        }
        
        const commandOutput = document.getElementById('command-output');
        commandOutput.style.display = 'block';
        const commandId = generateCommandId();
        lastCommandIdSent = commandId;
        
        commandOutput.innerHTML = `
            <div class="command-header"><div class="command-spinner"></div><span>Exécution de la commande: <span style="color: #38bdf8; margin-left: 5px;">${command}</span></span></div>
            <p>Veuillez patienter...</p>
        `;

        fetch(`/client/${clientId}/command`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                command: command, 
                command_id: commandId,
                button_type: buttonType 
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erreur réseau: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            setTimeout(() => {
                checkCommandResult(clientId);
            }, 2000);
        })
        .catch(error => {
            console.error("Erreur lors de l'envoi de la commande:", error);
            commandOutput.innerHTML = `
                <div class="command-header" style="color: #fb7185">Erreur lors de l'envoi de la commande</div>
                <p>${error.message || 'Une erreur est survenue'}</p>
            `;
        });
        
        return true;
    }

    // Fonction pour récupérer l'historique des commandes
    function fetchCommandHistory(clientId, buttonType = null) {
        if (!clientId) {
            return;
        }
        
        let url = `/client/${clientId}/command_history`;
        if (buttonType) {
            url += `?button_type=${buttonType}`;
        }
        
        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erreur réseau: ${response.status}`);
                }
                return response.json();
            });
    }

    // Modifions les listeners des boutons pour utiliser la nouvelle fonction
    executeCommandButton.addEventListener('click', function() {
        const command = commandInput.value;
        if (!command) {
            return; // Ne rien faire si aucune commande n'est entrée
        }
        
        if (!currentClientId) {
            // Au lieu d'afficher une alerte, mettre à jour directement le résultat pour indiquer qu'il faut sélectionner un appareil
            const commandOutput = document.getElementById('command-output');
            commandOutput.style.display = 'block';
            commandOutput.innerHTML = `
                <div class="command-header" style="color: #fb7185">Action impossible</div>
                <p>Sélectionnez un appareil dans la liste.</p>
            `;
            return;
        }
        
        sendCommandWithButton(currentClientId, command, 'Manual');
        commandInput.value = '';
    });

    // Fonction pour créer un dialogue personnalisé (remplace alert et confirm)
    function showCustomDialog(message, onConfirm = null, onCancel = null, isConfirm = false) {
        // Créer l'élément de dialogue
        const dialogEl = document.createElement('div');
        dialogEl.className = 'custom-dialog';
        
        // Contenu du dialogue
        let dialogContent = `
            <div class="dialog-content">
                <div class="dialog-message">${message}</div>
                <div class="dialog-buttons">
        `;
        
        // Ajouter les boutons selon le type (confirm ou alert)
        if (isConfirm) {
            dialogContent += `
                    <button class="dialog-button dialog-button-confirm" id="dialog-confirm-btn">Confirmer</button>
                    <button class="dialog-button dialog-button-cancel" id="dialog-cancel-btn">Annuler</button>
            `;
        } else {
            dialogContent += `
                    <button class="dialog-button dialog-button-confirm" id="dialog-ok-btn">OK</button>
            `;
        }
        
        dialogContent += `
                </div>
            </div>
        `;
        
        dialogEl.innerHTML = dialogContent;
        document.body.appendChild(dialogEl);
        
        // Ajouter les gestionnaires d'événements
        if (isConfirm) {
            const confirmBtn = document.getElementById('dialog-confirm-btn');
            const cancelBtn = document.getElementById('dialog-cancel-btn');
            
            confirmBtn.addEventListener('click', function() {
                if (onConfirm) onConfirm();
                document.body.removeChild(dialogEl);
            });
            
            cancelBtn.addEventListener('click', function() {
                if (onCancel) onCancel();
                document.body.removeChild(dialogEl);
            });
        } else {
            const okBtn = document.getElementById('dialog-ok-btn');
            
            okBtn.addEventListener('click', function() {
                if (onConfirm) onConfirm();
                document.body.removeChild(dialogEl);
            });
        }
    }
    
    // Power Off button functionality
    PowerOffCommandButton.addEventListener('click', function() {
        if (!currentClientId) {
            return; // Ne rien faire si aucun client n'est sélectionné
        }
        
        showCustomDialog("Voulez-vous vraiment éteindre cet appareil?", function() {
            // Code à exécuter si l'utilisateur confirme
            const commandOutput = document.getElementById('command-output');
            commandOutput.style.display = 'block';
            commandOutput.innerHTML = `
                <div class="command-header">
                    <div class="command-spinner"></div>
                    Extinction de l'appareil...
                </div>
                <p>Veuillez patienter...</p>
            `;
            
            // Get OS type from the server
            fetch(`/client/${currentClientId}`)
                .then(response => response.json())
                .then(clientData => {
                    const osType = clientData.os_type;
                    
                    let powerOffCommand;
                    switch (osType) {
                        case "Windows":
                            powerOffCommand = "shutdown /s /t 30 /c \"Arrêt à distance demandé par Ghost Spy - Vous avez 30 secondes pour annuler avec 'shutdown /a'\"";
                            break;
                        case "Linux":
                            powerOffCommand = "sudo shutdown -h +0.5 \"Arrêt à distance demandé par Ghost Spy - Vous avez 30 secondes pour annuler\"";
                            break;
                        case "Darwin": // macOS
                            powerOffCommand = "sudo shutdown -h +0.5";
                            break;
                        default:
                            powerOffCommand = "shutdown /s /t 30";
                    }
                    
                    sendCommandWithButton(currentClientId, powerOffCommand, "PowerOff");
                })
                .catch(error => {
                    console.error("Erreur lors de la récupération des données client:", error);
                    commandOutput.innerHTML = `
                        <div class="command-header" style="color: #fb7185">
                            Erreur lors de la récupération des données client
                        </div>
                        <p>${error.message || 'Une erreur est survenue'}</p>
                    `;
                });
        }, null, true);
    });
    
    // Cancel Shutdown button
    const cancelShutdownButton = document.getElementById('Cancel-Shutdown-button');
    if (cancelShutdownButton) {
        cancelShutdownButton.addEventListener('click', function() {
            if (!currentClientId) {
                return; // Ne rien faire si aucun client n'est sélectionné
            }
            
            const commandOutput = document.getElementById('command-output');
            commandOutput.style.display = 'block';
            commandOutput.innerHTML = `
                <div class="command-header">
                    <div class="command-spinner"></div>
                    Annulation de l'extinction...
                </div>
                <p>Veuillez patienter...</p>
            `;
            
            // Get OS type from the server
            fetch(`/client/${currentClientId}`)
                .then(response => response.json())
                .then(clientData => {
                    const osType = clientData.os_type;
                    let cancelCommand;
                    
                    switch (osType) {
                        case "Windows":
                            cancelCommand = "shutdown /a";
                            break;
                        case "Linux":
                            cancelCommand = "sudo shutdown -c \"Arrêt système annulé\"";
                            break;
                        case "Darwin": // macOS
                            cancelCommand = "sudo killall shutdown";
                            break;
                        default:
                            cancelCommand = "shutdown /a";
                    }
                    
                    sendCommandWithButton(currentClientId, cancelCommand, "CancelShutdown");
                })
                .catch(error => {
                    console.error("Erreur lors de la récupération des données client:", error);
                    commandOutput.innerHTML = `
                        <div class="command-header" style="color: #fb7185">
                            Erreur lors de la récupération des données client
                        </div>
                        <p>${error.message || 'Une erreur est survenue'}</p>
                    `;
                });
        });
    }

    // Add event listener for Freeze button
    const freezeButton = document.getElementById('Freeze-command-button');
    if (freezeButton) {
        freezeButton.addEventListener('click', function() {
            if (!currentClientId) {
                return; // Ne rien faire si aucun client n'est sélectionné
            }
            
            sendCommandWithButton(currentClientId, "freeze", "Freeze");
        });
    }

    // Add event listener for Unfreeze button
    const unfreezeButton = document.getElementById('Unfreeze-command-button');
    if (unfreezeButton) {
        unfreezeButton.addEventListener('click', function() {
            if (!currentClientId) {
                return; // Ne rien faire si aucun client n'est sélectionné
            }
            
            sendCommandWithButton(currentClientId, "unfreeze", "Unfreeze");
        });
    }

    executeAPIbutton.addEventListener('click', function() {
        const token = apiInput.value;
        if (!token) {
            return; // Ne rien faire si aucun token n'est entré
        }
        
        if (!currentClientId) {
            // Au lieu d'afficher une alerte, mettre à jour directement le résultat pour indiquer qu'il faut sélectionner un appareil
            const commandOutput = document.getElementById('api-output');
            commandOutput.style.display = 'block';
            commandOutput.innerHTML = `
                <div class="command-header" style="color: #fb7185">
                    Action impossible
                </div>
                <p>Sélectionnez un appareil dans la liste.</p>
            `;
            return;
        }
        
        const commandOutput = document.getElementById('api-output');
        commandOutput.style.display = 'block';
        commandOutput.innerHTML = `
            <div class="command-header">
                <div class="command-spinner"></div>
                Exécution de la commande: <span style="color: #38bdf8">${token}</span>
            </div>
            <p>Veuillez patienter...</p>
        `;
        
        fetch(`/client/${currentClientId}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token: token })
        })
        .then(response => response.json())
        .then(data => {
            console.log("OK")
            setTimeout(() => {
                commandOutput.innerHTML ='<p>Api mis a jour</p>'
            }, 2000);
            commandInput.value = '';
        })
        .catch(error =>{ console.log("Error")
            commandOutput.innerHTML = `
                <div class="command-header" style="color: #fb7185">
                    Erreur lors de l'envoi de la commande
                </div>
                <p>${error.message || 'Une erreur est survenue'}</p>
            `;
        });
    });

    function checkCommandResult(clientId) {
        fetch(`/client/${clientId}/commandresult`)
        .then(response => response.json())
        .then(data => {
            const commandOutput = document.getElementById('command-output');
            if (data.output && data.output.command_id === lastCommandIdSent) {
                let resultHtml = `
                    <div class="command-header">Commande : <span style="color: #38bdf8; margin-left: 5px;">${data.output.command}</span></div>`;

                if (data.output.stdout && data.output.stdout.trim() !== '') {
                    resultHtml += `
                        <div><div style="color: #94a3b8; margin-top: 10px; font-weight: bold;">STDOUT :</div><pre class="command-stdout">${escapeHtml(data.output.stdout)}</pre></div>`;
                } else {
                    resultHtml += `<div style="color: #94a3b8; margin-top: 10px; font-weight: bold;">STDOUT : (Pas de sortie)</div>`;
                }

                if (data.output.stderr && data.output.stderr.trim() !== '') {
                    resultHtml += `
                        <div><div style="color: #94a3b8; margin-top: 10px; font-weight: bold;">STDERR :</div><pre class="command-stderr">${escapeHtml(data.output.stderr)}</pre></div>`;
                }

                commandOutput.innerHTML = resultHtml;
            } else {
                commandOutput.innerHTML = `
                    <div class="command-header">
                        <div class="command-spinner"></div>
                        Attente de la réponse...
                    </div>
                    <p>L'exécution de la commande est en cours, veuillez patienter.</p>
                `;
                setTimeout(() => checkCommandResult(clientId), 1500);
            }
        })
        .catch(error => {
            const commandOutput = document.getElementById('command-output');
            commandOutput.innerHTML = `
                <div class="command-header" style="color: #fb7185">
                    Erreur lors de la récupération du résultat
                </div>
                <p>${error.message || 'Une erreur est survenue'}</p>
            `;
        });
    }

    function escapeHtml(unsafe) {
        if (!unsafe) return '';
        
        // Préserver les sauts de ligne tout en échappant les caractères spéciaux
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;")
            .replace(/\n/g, "<br>")   // Convertir les sauts de ligne en <br>
            .replace(/\s\s/g, "&nbsp;&nbsp;"); // Préserver les espaces multiples
    }

    setInterval(fetchClients, 5000);
    fetchClients();

    function percentageToDegrees(percent) {
        return percent * 3.6;
    }

    function fetchResourceInfo(clientId) {
        fetch(`/client/${clientId}/resources`)
            .then(response => response.json())
            .then(data => {
                if (data.resources) {
                    const cpuUsage = data.resources.cpu_usage;
                    const ramUsage = data.resources.ram_percent;
                    const cpuThresholdExceeded = data.resources.cpu_threshold_exceeded;
                    const ramThresholdExceeded = data.resources.ram_threshold_exceeded;

                    const cpuCircle = document.getElementById('cpu-progress');
                    const cpuPercentageText = document.getElementById('cpu-usage-text');
                    const cpuAlertText = document.getElementById('cpu-alert');

                    let cpuColor = cpuUsage > 80 ? '#ff3333' : cpuUsage > 60 ? '#ff9933' : '#4CAF50';
                    cpuCircle.style.background = `conic-gradient(${cpuColor} ${percentageToDegrees(cpuUsage)}deg, #e2e8f0 0deg)`;
                    cpuPercentageText.textContent = cpuUsage + '%';

                    if (cpuThresholdExceeded) {
                        cpuCircle.classList.add('pulse');
                        cpuAlertText.textContent = 'CPU dépasse le seuil maximal!';
                    } else {
                        cpuCircle.classList.remove('pulse');
                        cpuAlertText.textContent = '';
                    }

                    const ramCircle = document.getElementById('ram-progress');
                    const ramPercentageText = document.getElementById('ram-usage-text');
                    const ramAlertText = document.getElementById('ram-alert');

                    let ramColor = ramUsage > 80 ? '#ff3333' : ramUsage > 60 ? '#ff9933' : '#4CAF50';
                    ramCircle.style.background = `conic-gradient(${ramColor} ${percentageToDegrees(ramUsage)}deg, #e2e8f0 0deg)`;
                    ramPercentageText.textContent = ramUsage + '%';

                    if (ramThresholdExceeded) {
                        ramCircle.classList.add('pulse');
                        ramAlertText.textContent = 'RAM dépasse le seuil maximal!';
                    } else {
                        ramCircle.classList.remove('pulse');
                        ramAlertText.textContent = '';
                    }
                }
            })
            .catch(err => console.error('Error fetching resource info:', err));
    }

    function startResourcePolling(clientId) {
        resourcePollingInterval = setInterval(() => {
            fetchResourceInfo(clientId);
        }, 5000);
    }

    function stopResourcePolling() {
        clearInterval(resourcePollingInterval);
    }

    function startLogsPolling(clientId) {
        fetchLogs(clientId);
        logsPollingInterval = setInterval(() => {
            fetchLogs(clientId);
        }, 5000);
    }

    function stopLogsPolling() {
        clearInterval(logsPollingInterval);
    }

    function fetchLogs(clientId) {
        fetch(`/client/${clientId}/logs`)
            .then(response => response.json())
            .then(data => {
                if (data.logs && Array.isArray(data.logs)) {
                    displayLogs(data.logs);
                }
            })
            .catch(error => console.error('Erreur lors de la récupération des logs:', error));
    }

    function displayLogs(logs) {
        const logsContainer = document.getElementById('logs-container');
        
        // Trier les logs par horodatage
        logs.sort((a, b) => {
            return new Date(a.timestamp) - new Date(b.timestamp);
        });
        
        // S'il n'y a pas d'horodatage de dernier log traité, vider le conteneur
        if (!lastProcessedLogTime) {
            logsContainer.innerHTML = "";
        }
        
        // Filtrer les nouveaux logs
        const newLogs = logs.filter(log => !lastProcessedLogTime || log.timestamp > lastProcessedLogTime);
        
        if (newLogs.length > 0) {
            // Mettre à jour l'horodatage du dernier log traité
            lastProcessedLogTime = logs[logs.length - 1].timestamp;
            
            // Ajouter les nouveaux logs au conteneur
            newLogs.forEach(log => {
                const logElement = createLogElement(log);
                logsContainer.appendChild(logElement);
            });
            
            // Faire défiler jusqu'au bas
            logsContainer.scrollTop = logsContainer.scrollHeight;
        } else if (logs.length > 0 && logsContainer.innerHTML === "") {
            // Si aucun nouveau log mais le conteneur est vide, afficher tous les logs
            logs.forEach(log => {
                const logElement = createLogElement(log);
                logsContainer.appendChild(logElement);
            });
            logsContainer.scrollTop = logsContainer.scrollHeight;
        }
    }

    function createLogElement(log) {
        const logEntry = document.createElement('div');
        
        // Déterminer le type d'élément (fichier, dossier, exécutable)
        let elementType = 'file';
        if (log.message.includes('dossier')) {
            elementType = 'folder';
        } else if (log.message.includes('exécutable') || log.message.includes('Exécutable')) {
            elementType = 'exe';
        }
        
        // Déterminer le type d'action (création, modification, suppression, déplacement)
        let actionType = 'Création';
        if (log.message.includes('modifié')) {
            actionType = 'Modification';
        } else if (log.message.includes('supprimé')) {
            actionType = 'Suppression';
        } else if (log.message.includes('déplacé') || log.message.includes('renommé')) {
            actionType = 'Déplacement';
        }
        
        // Définir la classe CSS en fonction du type d'élément et si c'est un avertissement
        const elementClass = `log-entry log-entry-${elementType}`;
        logEntry.className = log.level === 'WARNING' ? elementClass + ' log-entry-warning' : elementClass;
        
        // Ajouter des attributs de données pour le filtrage
        logEntry.setAttribute('data-element-type', elementType);
        logEntry.setAttribute('data-log-type', actionType);
        
        // Extraire le nom du fichier et le chemin de l'élément du message
        const nameMatch = log.message.match(/(Nouveau |Nouvel |Fichier |Application )([^:]+):/);
        const pathMatch = log.message.match(/dans ([^$]+)$/);
        
        const name = nameMatch ? nameMatch[2] : 'Élément';
        const path = pathMatch ? pathMatch[1] : '';
        
        // Formater l'horodatage
        const timestamp = new Date(log.timestamp);
        const formattedTime = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        
        // Construire le contenu HTML
        let logContent = `
            <span class="log-time">[${formattedTime}]</span>
            <span class="log-type log-type-${getLogTypeClass(actionType)}">${actionType}</span>
            <span class="log-message">${log.message}</span>
        `;
        
        logEntry.innerHTML = logContent;
        return logEntry;
    }

    function getLogTypeClass(type) {
        return type.toLowerCase()
            .replace('é', 'e')
            .replace('è', 'e')
            .replace('ê', 'e')
            .replace('à', 'a')
            .replace('ç', 'c');
    }

    const filterCheckboxes = document.querySelectorAll('.logs-filter input[type="checkbox"]');
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', applyLogFilters);
    });

    function applyLogFilters() {
        const logEntries = document.querySelectorAll('.log-entry');
        const showFile = document.getElementById('filter-file').checked;
        const showFolder = document.getElementById('filter-folder').checked;
        const showExe = document.getElementById('filter-exe').checked;
        const showCreated = document.getElementById('filter-created').checked;
        const showModified = document.getElementById('filter-modified').checked;
        const showDeleted = document.getElementById('filter-deleted').checked;
        const showMoved = document.getElementById('filter-moved').checked;

        logEntries.forEach(entry => {
            const elementType = entry.getAttribute('data-element-type');
            const logType = entry.getAttribute('data-log-type');
            let showEntry = true;
            if (elementType === 'file' && !showFile) showEntry = false;
            if (elementType === 'folder' && !showFolder) showEntry = false;
            if (elementType === 'exe' && !showExe) showEntry = false;
            if (logType === 'Création' && !showCreated) showEntry = false;
            if (logType === 'Modification' && !showModified) showEntry = false;
            if (logType === 'Suppression' && !showDeleted) showEntry = false;
            if (logType === 'Déplacement' && !showMoved) showEntry = false;
            entry.style.display = showEntry ? 'block' : 'none';
        });
    }

    function fetchScanResults(clientId) {
        fetch(`/client/${clientId}/virus_scans`)
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('scan-results-container');
                container.innerHTML = '';

                if (!data.scans || data.scans.length === 0) {
                    container.innerHTML = '<p>Aucun fichier scanné récemment</p>';
                    return;
                }

                // Créer un en-tête pour les résultats
                const headerDiv = document.createElement('div');
                headerDiv.innerHTML = `<h4>Résultats de scan VirusTotal (${data.scans.length} fichiers)</h4>`;
                headerDiv.className = 'scan-header';
                container.appendChild(headerDiv);

                // Trier les scans par date de scan (plus récent en premier)
                const sortedScans = data.scans.sort((a, b) => new Date(b.scan_date) - new Date(a.scan_date));
                
                sortedScans.forEach(scan => {
                    const resultDiv = document.createElement('div');
                    
                    // Déterminer le statut et la couleur
                    let status = '';
                    let statusIcon = '';
                    let statusClass = '';
                    
                    if (scan.status === 'error') {
                        status = `❌ Erreur: ${scan.error_message || 'Erreur inconnue'}`;
                        statusClass = 'error';
                    } else if (scan.status === 'quota_exceeded') {
                        status = '⚠️ Quota VirusTotal dépassé';
                        statusClass = 'warning';
                    } else if (scan.status === 'pending') {
                        status = '⏳ Analyse en cours...';
                        statusClass = 'pending';
                    } else if (scan.status === 'complete' && scan.result) {
                        const isMalicious = scan.result.is_malicious;
                        const maliciousCount = scan.result.malicious || 0;
                        const suspiciousCount = scan.result.suspicious || 0;
                        const totalEngines = scan.result.total_engines || 0;
                        
                        if (isMalicious) {
                            statusIcon = '🦠';
                            status = `Malveillant (${maliciousCount + suspiciousCount}/${totalEngines} détections)`;
                            statusClass = 'malicious';
                        } else {
                            statusIcon = '✅';
                            status = `Sécurisé (0/${totalEngines} détections)`;
                            statusClass = 'clean';
                        }
                    } else {
                        status = '❓ Statut inconnu';
                        statusClass = 'unknown';
                    }
                    
                    resultDiv.className = `scan-result ${statusClass}`;
                    resultDiv.innerHTML = `
                        <div class="scan-file-info">
                            <h5>${statusIcon} ${scan.file_name || 'Fichier inconnu'}</h5>
                            <p><strong>Statut:</strong> ${status}</p>
                            <p><strong>Date de scan:</strong> ${new Date(scan.scan_date).toLocaleString()}</p>
                            ${scan.file_hash ? `<p><strong>Hash SHA256:</strong> <code>${scan.file_hash.substring(0, 16)}...</code></p>` : ''}
                        </div>
                    `;
                    
                    // Ajouter les détails de détection si disponibles
                    if (scan.status === 'complete' && scan.result && scan.result.detected_engines) {
                        const detailsDiv = document.createElement('div');
                        detailsDiv.className = 'scan-details';
                        detailsDiv.innerHTML = '<h6>Moteurs ayant détecté des menaces:</h6>';
                        
                        const enginesList = document.createElement('ul');
                        Object.entries(scan.result.detected_engines).forEach(([engine, data]) => {
                            const listItem = document.createElement('li');
                            listItem.innerHTML = `<strong>${engine}:</strong> ${data.result} (${data.category})`;
                            enginesList.appendChild(listItem);
                        });
                        detailsDiv.appendChild(enginesList);
                        resultDiv.appendChild(detailsDiv);
                    }
                    
                    // Ajouter les informations de vérification locale si disponibles
                    if (scan.local_check) {
                        const localDiv = document.createElement('div');
                        localDiv.className = 'local-check';
                        localDiv.innerHTML = `
                            <h6>Analyse locale:</h6>
                            <p><strong>Suspect:</strong> ${scan.local_check.suspicious ? 'Oui' : 'Non'}</p>
                            ${scan.local_check.reasons && scan.local_check.reasons.length > 0 ? 
                                `<p><strong>Raisons:</strong> ${scan.local_check.reasons.join(', ')}</p>` : ''}
                        `;
                        resultDiv.appendChild(localDiv);
                    }
                    
                    container.appendChild(resultDiv);
                });
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des résultats VirusTotal:', error);
                const container = document.getElementById('scan-results-container');
                container.innerHTML = `
                    <div class="scan-error">
                        <h4>❌ Erreur lors de la récupération des fichiers suspects</h4>
                        <p>Impossible de charger les résultats de scan VirusTotal.</p>
                        <p>Détails: ${error.message || 'Erreur de connexion'}</p>
                    </div>
                `;
            });
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function startScanResultsPolling(clientId) {
        scanResultsPollingInterval = setInterval(() => {
            fetchScanResults(clientId);
        }, 10000); // Poll every 10 seconds
    }

    function stopScanResultsPolling() {
        clearInterval(scanResultsPollingInterval);
    }

    // Add CSS for scan detection details
    const style = document.createElement('style');
    style.textContent = `
        .scan-header {
            background-color: #f7fafc;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 15px;
            border-left: 4px solid #3b82f6;
        }
        
        .scan-header h4 {
            margin: 0;
            color: #2d3748;
            font-size: 16px;
        }
        
        .scan-result {
            background-color: #f8faff;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            border-left: 4px solid #3b82f6;
        }
        
        .scan-result.malicious {
            background-color: #fff5f5;
            border-left-color: #e53e3e;
        }
        
        .scan-result.clean {
            border-left-color: #38a169;
            background-color: #f0fff4;
        }
        
        .scan-result.error {
            background-color: #fffaf0;
            border-left-color: #ed8936;
        }
        
        .scan-result.warning {
            background-color: #fffbeb;
            border-left-color: #f59e0b;
        }
        
        .scan-result.pending {
            background-color: #f0f9ff;
            border-left-color: #0ea5e9;
        }
        
        .scan-result.unknown {
            background-color: #f9fafb;
            border-left-color: #6b7280;
        }
        
        .scan-file-info h5 {
            margin-top: 0;
            margin-bottom: 10px;
            color: #4a5568;
            font-size: 16px;
            font-weight: 600;
        }
        
        .scan-result.malicious .scan-file-info h5 {
            color: #e53e3e;
        }
        
        .scan-result.clean .scan-file-info h5 {
            color: #38a169;
        }
        
        .scan-result.error .scan-file-info h5 {
            color: #ed8936;
        }
        
        .scan-result.warning .scan-file-info h5 {
            color: #f59e0b;
        }
        
        .scan-file-info p {
            margin: 5px 0;
            font-size: 14px;
            color: #4a5568;
        }
        
        .scan-file-info code {
            background-color: #e2e8f0;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            color: #2d3748;
        }
        
        .scan-details {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e2e8f0;
        }
        
        .scan-details h6 {
            margin: 0 0 10px 0;
            color: #2d3748;
            font-size: 14px;
            font-weight: 600;
        }
        
        .scan-details ul {
            margin: 0;
            padding-left: 20px;
            list-style-type: disc;
        }
        
        .scan-details li {
            margin: 5px 0;
            font-size: 13px;
            color: #4a5568;
        }
        
        .local-check {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e2e8f0;
            background-color: rgba(99, 102, 241, 0.05);
            border-radius: 6px;
            padding: 10px;
        }
        
        .local-check h6 {
            margin: 0 0 8px 0;
            color: #5b21b6;
            font-size: 14px;
            font-weight: 600;
        }
        
        .local-check p {
            margin: 5px 0;
            font-size: 13px;
            color: #5b21b6;
        }
        
        .scan-error {
            background-color: #fff5f5;
            border: 1px solid #feb2b2;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }
        
        .scan-error h4 {
            margin-top: 0;
            color: #e53e3e;
            font-size: 18px;
        }
        
        .scan-error p {
            margin: 8px 0;
            color: #4a5568;
            font-size: 14px;
        }
        
        .malware-scan-area {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            border: 1px solid #e2e8f0;
        }
        
        .malware-scan-area h3 {
            margin-top: 0;
            margin-bottom: 20px;
            color: #2d3748;
            font-size: 18px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .malware-scan-area h3:before {
            content: "🛡️";
            font-size: 20px;
        }
    `;
    document.head.appendChild(style);
    
    function loadScanResults(clientId) {
        fetch(`/client/${clientId}/scan_results`)
            .then(response => response.json())
            .then(data => {
                const scanResultsContainer = document.getElementById('scan-results-container');
                scanResultsContainer.innerHTML = '';
                
                if (data.malicious_files && data.malicious_files.length > 0) {
                    // Display malicious files first
                    const malwareHeader = document.createElement('div');
                    malwareHeader.className = 'malware-warning';
                    malwareHeader.innerHTML = `<h4>⚠️ ${data.malicious_files.length} fichier(s) malveillant(s) détecté(s)</h4>`;
                    scanResultsContainer.appendChild(malwareHeader);
                    
                    data.malicious_files.forEach(file => {
                        const fileElement = createScanResultElement(file, true);
                        scanResultsContainer.appendChild(fileElement);
                    });
                }
                
                // Display all recent scans
                if (data.scan_results && data.scan_results.length > 0) {
                    const recentHeader = document.createElement('div');
                    recentHeader.className = 'recent-scans-header';
                    recentHeader.innerHTML = '<h4>Scans récents</h4>';
                    scanResultsContainer.appendChild(recentHeader);
                    
                    data.scan_results.forEach(file => {
                        // Avoid repeating malicious files already displayed
                        if (!file.is_malicious) {
                            const fileElement = createScanResultElement(file, false);
                            scanResultsContainer.appendChild(fileElement);
                        }
                    });
                } else {
                    scanResultsContainer.innerHTML = '<p>Aucun fichier scanné récemment</p>';
                }
            })
            .catch(error => {
                console.error('Erreur lors du chargement des résultats de scan:', error);
                document.getElementById('scan-results-container').innerHTML = 
                    '<p>Erreur lors du chargement des résultats de scan</p>';
            });
    }

    function createScanResultElement(fileData, isHighlighted) {
        const fileElement = document.createElement('div');
        fileElement.className = `scan-result ${isHighlighted ? 'malicious' : 'safe'}`;
        
        // Format the date
        const scanDate = new Date(fileData.scan_date);
        const formattedDate = scanDate.toLocaleString();
        
        // Detections
        const detections = fileData.details && fileData.details.detections ? fileData.details.detections : 0;
        const totalEngines = fileData.details && fileData.details.total ? fileData.details.total : 0;
        
        // Build the display content
        let contentHTML = `
            <div class="file-info">
                <div class="file-name">${fileData.file_name}</div>
                <div class="file-path">${fileData.path || ''}</div>
                <div class="scan-date">Scanné le: ${formattedDate}</div>
            </div>
            <div class="scan-status">
        `;
        
        if (fileData.is_malicious) {
            contentHTML += `<div class="status-icon malicious">☠️</div>
                           <div class="status-text">Malveillant (${detections}/${totalEngines})</div>`;
        } else {
            contentHTML += `<div class="status-icon safe">✅</div>
                           <div class="status-text">Sécurisé (0/${totalEngines})</div>`;
        }
        
        contentHTML += `</div>`;
        fileElement.innerHTML = contentHTML;
        
        return fileElement;
    }

    // Event listeners for PDF buttons
    checkPdfButton.addEventListener('click', function() {
        if (currentClientId) {
            checkPdfExists(currentClientId);
        }
    });
    
    generatePdfButton.addEventListener('click', function() {
        if (currentClientId) {
            generatePdfReport(currentClientId);
        }
    });
    
    downloadPdfButton.addEventListener('click', function() {
        if (currentClientId && pdfExists) {
            downloadPdfReport(currentClientId);
        }
    });

    // Function to check if PDF exists
    function checkPdfExists(clientId) {
        pdfStatusDiv.className = '';
        pdfStatusDiv.innerHTML = '<div class="command-spinner"></div> Vérification du rapport PDF...';
        
        fetch(`/client/${clientId}/check_pdf_exists`)
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    pdfExists = true;
                    pdfStatusDiv.className = 'pdf-status-success';
                    pdfStatusDiv.textContent = 'Rapport PDF disponible.';
                    generatePdfButton.style.display = 'none';
                    downloadPdfButton.style.display = 'inline-block';
                } else {
                    pdfExists = false;
                    pdfStatusDiv.className = 'pdf-status-info';
                    pdfStatusDiv.textContent = 'Aucun rapport PDF disponible. Veuillez générer un rapport.';
                    generatePdfButton.style.display = 'inline-block';
                    downloadPdfButton.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error checking PDF existence:', error);
                pdfStatusDiv.className = 'pdf-status-error';
                pdfStatusDiv.textContent = 'Erreur lors de la vérification du rapport PDF.';
            });
    }
    
    // Function to generate PDF report
    function generatePdfReport(clientId) {
        pdfStatusDiv.className = '';
        pdfStatusDiv.innerHTML = '<div class="command-spinner"></div> Génération du rapport PDF en cours...';
        generatePdfButton.disabled = true;
        
        fetch(`/client/${clientId}/generate_pdf`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('PDF generation initiated:', data);
            pdfStatusDiv.className = 'pdf-status-info';
            pdfStatusDiv.textContent = 'Génération en cours... Cela peut prendre quelques instants.';
            
            // Poll for command completion
            const commandId = data.command_id;
            if (commandId) {
                const checkInterval = setInterval(() => {
                    fetch(`/client/${clientId}/command_history?button_type=PDFReport`)
                        .then(response => response.json())
                        .then(history => {
                            const pdfCommand = history.find(cmd => cmd.command_id === commandId);
                            if (pdfCommand && pdfCommand.status !== 'pending') {
                                clearInterval(checkInterval);
                                generatePdfButton.disabled = false;
                                
                                if (pdfCommand.status === 'success') {
                                    // Wait a few seconds to ensure PDF is uploaded
                                    setTimeout(() => {
                                        checkPdfExists(clientId);
                                    }, 3000);
                                } else {
                                    pdfStatusDiv.className = 'pdf-status-error';
                                    pdfStatusDiv.textContent = 'Échec de la génération du rapport PDF.';
                                }
                            }
                        })
                        .catch(error => {
                            console.error('Error checking PDF generation status:', error);
                        });
                }, 2000);
                
                // Stop checking after 1 minute if no response
                setTimeout(() => {
                    clearInterval(checkInterval);
                    generatePdfButton.disabled = false;
                    checkPdfExists(clientId);
                }, 60000);
            }
        })
        .catch(error => {
            console.error('Error initiating PDF generation:', error);
            pdfStatusDiv.className = 'pdf-status-error';
            pdfStatusDiv.textContent = 'Erreur lors de l\'initialisation de la génération du rapport.';
            generatePdfButton.disabled = false;
        });
    }
    
    // Function to download PDF report
    function downloadPdfReport(clientId) {
        window.location.href = `/client/${clientId}/download_pdf`;
    }
    
    // Initialize PDF status when viewing a device
    function initializePdfSection(clientId) {
        checkPdfExists(clientId);
    }

    // Modify showDevicePage function to include PDF initialization
    const originalShowDevicePage = window.showDevicePage;
    window.showDevicePage = function(clientId, clientName) {
        // Call the original function first
        if (typeof originalShowDevicePage === 'function') {
            originalShowDevicePage(clientId, clientName);
        } else {
            // Fallback if original function wasn't properly captured
            currentClientId = clientId;
            deviceNameHeader.textContent = clientName;
            devicePageDiv.style.display = 'block';
            clientListDiv.style.display = 'none';
            fetchScreenshot(clientId);
            startScreenshotPolling(clientId);
            fetchResourceInfo(clientId);
            startResourcePolling(clientId);
            startLogsPolling(clientId);
            fetchScanResults(clientId);
            startScanResultsPolling(clientId);
            loadCommandHistory(clientId);
            lastProcessedLogTime = null;
            localStorage.setItem('currentClientId', clientId);
            localStorage.setItem('currentClientName', clientName);
            enableCommandButtons();
            
            // Fetch and apply client settings
            fetch(`/client/${clientId}/settings/admin`)
                .then(response => response.json())
                .then(settings => {
                    applyFeatureVisibility(settings);
                })
                .catch(error => {
                    console.error("Erreur lors de la récupération des paramètres:", error);
                });
        }
        
        // Initialize PDF section
        initializePdfSection(clientId);
    };

    // Ajouter les événements pour les filtres d'historique
    document.addEventListener('DOMContentLoaded', function() {
        const historyFilterButtons = document.querySelectorAll('.history-filter-btn');
        historyFilterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Mettre à jour la classe active
                historyFilterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // Récupérer le filtre sélectionné
                const filter = this.getAttribute('data-filter');
                
                // Charger l'historique filtré
                if (currentClientId) {
                    if (filter === 'all') {
                        loadCommandHistory(currentClientId);
                    } else {
                        loadCommandHistory(currentClientId, filter);
                    }
                }
            });
        });
        
        // Recharger l'historique périodiquement
        setInterval(() => {
            if (currentClientId && devicePageDiv.style.display !== 'none') {
                const activeFilterBtn = document.querySelector('.history-filter-btn.active');
                const filter = activeFilterBtn ? activeFilterBtn.getAttribute('data-filter') : 'all';
                
                if (filter === 'all') {
                    loadCommandHistory(currentClientId);
                } else {
                    loadCommandHistory(currentClientId, filter);
                }
            }
        }, 10000); // Mise à jour toutes les 10 secondes
    });
});

function openClientSettings(clientId) {
    window.location.href = `settings.html?client_id=${clientId}`;
}

// Adapter la fonction qui affiche les clients pour inclure un bouton Settings
function displayClients(clients) {
    const clientList = document.getElementById('clientList');
    clientList.innerHTML = '';
    
    clients.forEach(client => {
        // Autres éléments d'affichage existants...
        
        // Ajouter un bouton Settings
        const settingsButton = document.createElement('button');
        settingsButton.className = 'btn btn-info btn-sm';
        settingsButton.innerHTML = '<i class="material-icons">settings</i> Paramètres';
        settingsButton.onclick = function() {
            openClientSettings(client.id);
        };
        
        // Ajouter le bouton au conteneur des actions du client
        const actionsContainer = document.getElementById(`client-actions-${client.id}`);
        actionsContainer.appendChild(settingsButton);
    });
}

// Fonction pour appliquer les états visuels en fonction des paramètres activés/désactivés
function applyFeatureVisibility(settings) {
    // Système de ressources
    const resourcesArea = document.querySelector('.resources-area');
    toggleSectionVisibility(resourcesArea, settings.system_resources_enabled, "Surveillance des ressources désactivée");
    
    // Logs d'activité
    const logsArea = document.querySelector('.logs-area');
    toggleSectionVisibility(logsArea, settings.activity_logs_enabled, "Journalisation des activités désactivée");
    
    // Détection de fichiers suspects
    const malwareScanArea = document.querySelector('.malware-scan-area');
    toggleSectionVisibility(malwareScanArea, settings.file_detection_enabled, "Détection de fichiers suspects désactivée");
    
    // Si VirusTotal est désactivé mais la détection de fichiers est activée, afficher un message
    if (!settings.virustotal_enabled && settings.file_detection_enabled && malwareScanArea) {
        const vtWarning = document.createElement('div');
        vtWarning.className = 'alert alert-warning';
        vtWarning.textContent = 'L\'analyse VirusTotal est désactivée. Les fichiers suspects sont détectés mais pas analysés.';
        malwareScanArea.prepend(vtWarning);
    }
    
    // Afficher un résumé des fonctionnalités actives
    updateFeatureIndicators(settings);
}

function toggleSectionVisibility(element, isEnabled, disabledMessage) {
    if (!element) return;
    
    if (isEnabled) {
        element.classList.remove('disabled-section');
        // Supprimer l'icône si elle existe
        const existingIcon = element.querySelector('.disabled-icon');
        if (existingIcon) {
            element.removeChild(existingIcon);
        }
    } else {
        element.classList.add('disabled-section');
        
        // S'assurer qu'on n'ajoute pas plusieurs icônes
        if (!element.querySelector('.disabled-icon')) {
            const disabledIcon = document.createElement('div');
            disabledIcon.className = 'disabled-icon';
            disabledIcon.textContent = '✕';
            disabledIcon.title = disabledMessage;
            element.appendChild(disabledIcon);
        }
    }
}

function updateFeatureIndicators(settings) {
    const devicePage = document.getElementById('device-page');
    if (!devicePage) return;
    
    // Vérifier si le conteneur d'indicateurs existe déjà, sinon le créer
    let indicatorsContainer = devicePage.querySelector('.feature-indicators');
    if (!indicatorsContainer) {
        indicatorsContainer = document.createElement('div');
        indicatorsContainer.className = 'feature-indicators';
        
        // Insérer après le titre de l'appareil
        const deviceTitle = devicePage.querySelector('h2');
        if (deviceTitle && deviceTitle.nextSibling) {
            devicePage.insertBefore(indicatorsContainer, deviceTitle.nextSibling);
        } else {
            devicePage.prepend(indicatorsContainer);
        }
    } else {
        // Vider le conteneur existant
        indicatorsContainer.innerHTML = '';
    }
    
    // Créer les indicateurs de fonctionnalités
    const features = [
        { name: 'Ressources système', enabled: settings.system_resources_enabled },
        { name: 'Journaux d\'activité', enabled: settings.activity_logs_enabled },
        { name: 'Détection de fichiers', enabled: settings.file_detection_enabled },
        { name: 'Analyse VirusTotal', enabled: settings.virustotal_enabled }
    ];
    
    features.forEach(feature => {
        const indicator = document.createElement('div');
        indicator.className = `feature-indicator ${feature.enabled ? 'feature-enabled' : 'feature-disabled'}`;
        indicator.innerHTML = `<i>${feature.enabled ? '✓' : '✕'}</i> ${feature.name}`;
        indicatorsContainer.appendChild(indicator);
    });
}

// Pour s'assurer que les états visuels sont appliqués aussi lors du chargement initial de la page
// si un client est déjà sélectionné (depuis localStorage par exemple)
document.addEventListener('DOMContentLoaded', function() {
    // Vérifier si un client était précédemment sélectionné
    const savedClientId = localStorage.getItem('currentClientId');
    const savedClientName = localStorage.getItem('currentClientName');
    
    if (savedClientId && savedClientName) {
        showDevicePage(savedClientId, savedClientName);
    }
});