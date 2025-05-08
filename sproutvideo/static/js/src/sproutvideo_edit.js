function SproutVideoEditXBlock(runtime, element) {
    return {
        init: function() {
            const input = element.querySelector('#sproutvideo-url-input');
            const iframe = element.querySelector('#sproutvideo-preview');
            const saveButton = element.querySelector('.save-button');

            // Aktualizacja iframe
            input.addEventListener('input', () => {
                const url = input.value.trim();
                iframe.src = url;
            });

            saveButton.addEventListener('click', function () {
                const url = input.value.trim();

                if (!url.startsWith('https://videos.sproutvideo.com/embed/')) {
                    runtime.notify('error', {
                        msg: 'Niepoprawny adres URL. Wprowadź pełny embed URL ze SproutVideo.'
                    });
                    return;
                }

                runtime.notify('save', { state: 'start' });

                runtime.xblockHandler(element, 'save_video_url', {
                    method: 'POST',
                    data: JSON.stringify({ video_url: url })
                }).then(function () {
                    runtime.notify('save', { state: 'end' });
                }).catch(function (error) {
                    console.error("Błąd zapisu:", error);
                    runtime.notify('error', { msg: 'Zapis nie powiódł się.' });
                });
            });
        }
    };
}
