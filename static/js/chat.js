let chatId = null;
let chatSocket = null;
let chatField = null;

function chat_connect() {
    chatSocket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${chatId}/`);

    chatSocket.onopen = e => {
        console.log('[CHAT] WebSocket successfully connected!');
        if (chatId) {
            chatSocket.send(JSON.stringify({
                'type': 'get_messages',
                'chat_id': chatId,
            }))
            chatSocket.send(JSON.stringify({
                'type': 'get_users',
                'chat_id': chatId,
            }));
        }
    }

    chatSocket.onclose = e => {
        console.log('[CHAT] Lost connection to server');
    }

    chatSocket.onmessage = e => {
        const data = JSON.parse(e.data);

        switch (data.type) {
            case "message_send":
                createNewMessage(data);
                break;
            case 'get_messages':
                get_chat_messages(data['data'])
                console.log('[CHAT] Old messages successfully loaded');
                break;
            case "get_users":
                get_users_list(data);
                break;
            case "reload":
                location = '/';
                break;
            default:
                console.log(data)
                console.error('[CHAT] Unknown message type!');
                break;
        }
    }

    chatSocket.onerror = e => {
        console.log('[CHAT] Caught an error! Closing the socket');
    }
}

function selectChat(data) {
    document.querySelector('.selected-chat').className = 'chat-list-item';
    data.target.className += ' selected-chat';
    updateSelectedChatId();
    chatSocket.close();

    chat_connect();
}

function updateSelectedChatId() {
    chatId = document.querySelector('.selected-chat #chat_id').innerText;
}

function createNewMessage(data) {
    let messageElement = document.createElement('div');
    let infoElement = document.createElement('div');
    let textElement = document.createElement('div');
    messageElement.className = 'message';
    infoElement.className = 'info';
    textElement.className = 'text';

    if (userId === data.user_id) {
        messageElement.className += ' reverse';
    }

    textElement.innerHTML = data.message;
    infoElement.innerHTML = `<div class="img"><img alt="user's avatar" src="${data.avatar}"></div>
                             <div class="nickname">${data.user_nickname}</div>`;
    messageElement.append(infoElement);
    messageElement.append(textElement);

    chatField.appendChild(messageElement);
    setTimeout(() => {
        chatField.scrollTop = chatField.scrollHeight;
    }, 100);
}

function get_chat_messages(data) {
    chatField.innerHTML = '';
    for (let i = 0; i < data.length; i++) {
        createNewMessage(data[i]);
    }
}

function createChat() {
    let title = prompt('Введите название чата');
    if (title === null) {
        return null;
    }
    else if (title.length <= 5) {
        alert('Название слишком короткое, необходимо хотя бы 5 символов');
        return null;
    }
    let chatCreateSocket = new WebSocket('ws://127.0.0.1:8000/ws/chat-create/');

    chatCreateSocket.onopen = e => {
        console.log('[CREATE-CHAT] Socket has been opened');
        chatCreateSocket.send(JSON.stringify({
            "type": 'create_chat',
            'title': title,
            'user_id': userId,
        }));
    }
    chatCreateSocket.onmessage = e => {
        const data = JSON.parse(e.data)
        switch (data.type) {
            case 'chat_created':
                location = '/';
                break;
            default:
                console.log('[CREATE-CHAT] Got unknown message type');
                break;
        }
        chatCreateSocket.close();
    }
}

function get_users_list(data) {
    let nodeElement = document.querySelector('#users-list');
    let newElement = null;
    nodeElement.innerHTML = '';
    for (let i = 0; i < data.data.length; i++) {
        newElement = document.createElement('div');
        newElement.className = 'users-list-item';
        newElement.innerHTML = `
        <div class="img"><img alt="user's avatar" src="${data.data[i].avatar}"></div>
        <div class="nickname">${data.data[i].nickname}</div>
        `;
        nodeElement.appendChild(newElement);
    }
}

function change_user(data) {
    let textInputValue = parseInt(document.querySelector('.text-input').value);
    if (!textInputValue) {
        alert('Введите корректное целое число!');
        return null;
    }
    console.log(data.target.name);
    chatSocket.send(JSON.stringify({
        "type": data.target.name,
        "user_id": textInputValue,
        "chat_id": chatId,
    }));
    document.querySelector('.text-input').value = '';
}

window.onload = () => {
    let textInput = document.querySelector('#textInput');
    textInput.focus();
    let sendButton = document.querySelector('#sendButton');
    chatField = document.querySelector('#chat')

    document.querySelector('#chat-create-button').onclick = createChat;
    let firstChatItem = document.querySelector('.chat-list-item')
    if (firstChatItem) {
        firstChatItem.className += ' selected-chat';
        updateSelectedChatId();
        document.querySelector('#add-user').onclick = change_user;
        document.querySelector('#remove-user').onclick = change_user;
    }

    let elements = document.getElementsByClassName('chat-list-item')
    for (let i = 0; i < elements.length; i++) {
        elements[i].onclick = selectChat;
    }

    sendButton.onclick = () => {
        if (textInput.value.length === 0) return;
        if (chatId === null) return;

        chatSocket.send(JSON.stringify({
            "type": 'send_message',
            "message":  textInput.value,
            "user_id": userId,
    }));

        textInput.value = "";
    }

    if (chatId) {
        chat_connect();
    } else {
        chatField.innerHTML = 'Выглядит как будто вы не состоите в каком либо чате';
    }
}