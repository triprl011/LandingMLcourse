document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('leadForm');
    const messageDiv = document.getElementById('formMessage');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();

        if (!email || !email.includes('@')) {
            messageDiv.style.color = '#dc2626';
            messageDiv.textContent = '⚠️ Введите корректный email';
            return;
        }

        try {
            const response = await fetch('/submit_lead', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email })
            });

            const data = await response.json();

            if (data.status === 'success') {
                messageDiv.style.color = '#16a34a';
                messageDiv.textContent = '✅ ' + data.message;
                form.reset();

                // Дополнительно открываем Telegram через 2 секунды
                setTimeout(() => {
                    window.open('https://t.me/your_manager_nastya', '_blank');
                }, 2000);
            } else {
                messageDiv.style.color = '#dc2626';
                messageDiv.textContent = '⚠️ ' + data.message;
            }
        } catch (error) {
            messageDiv.style.color = '#dc2626';
            messageDiv.textContent = '❌ Ошибка сервера. Попробуйте позже.';
        }
    });
});