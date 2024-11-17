document.addEventListener('DOMContentLoaded', () => {
    const checkButton = document.getElementById('checkButton');
    const sendButton = document.getElementById('sendButton');
    const messageGroup = document.getElementById('messageGroup');
    const webhookUrlInput = document.getElementById('webhookUrl');
    const messageInput = document.getElementById('message');
    let sending = false;

    checkButton.addEventListener('click', async () => {
        const webhookUrl = webhookUrlInput.value.trim();
        if (webhookUrl) {
            try {
                const response = await fetch(webhookUrl, { method: 'GET' });
                if (response.ok) {
                    checkButton.classList.add('valid');
                    checkButton.textContent = 'Valid!';
                    messageGroup.classList.remove('hidden');
                } else {
                    checkButton.classList.remove('valid');
                    checkButton.textContent = 'Invalid!';
                    alert('Invalid Webhook URL');
                }
            } catch (error) {
                checkButton.classList.remove('valid');
                checkButton.textContent = 'Invalid!';
                alert('Error: ' + error.message);
            }
        }
    });

    sendButton.addEventListener('click', async () => {
        if (sending) {
            sending = false;
            sendButton.textContent = 'Send';
            sendButton.classList.remove('stop');
            return;
        }

        const webhookUrl = webhookUrlInput.value.trim();
        const message = messageInput.value.trim();
        if (webhookUrl && message) {
            sending = true;
            sendButton.textContent = 'Stop';
            sendButton.classList.add('stop');

            while (sending) {
                try {
                    await fetch(webhookUrl, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ content: message })
                    });
                    await new Promise(resolve => setTimeout(resolve, 10));
                } catch (error) {
                    alert('Error: ' + error.message);
                    sending = false;
                    sendButton.textContent = 'Send';
                    sendButton.classList.remove('stop');
                }
            }
        }
    });
});
