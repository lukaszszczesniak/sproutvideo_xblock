function SproutVideoEditXBlock(runtime, element) {

            function initiallyValid(url) {
                const check = url.startsWith('https://videos.sproutvideo.com/embed/');
                if (!check) {
                    console.warn("Wstępne sprawdzenie nie powiodło się, url: ", url);
                }
                return check;
            }

            function updatePreviewUrl(url) {
                $('#sproutvideo-preview', element).attr("src", url);
                console.log("Zaktualizowano podląd na url: ", url);
            }

            function saveSucceed(response) {
                console.log("Zapis udany! ", response.url);
                updatePreviewUrl(response.url);
            }

            function saveFailed(jqXHR, textStatus, errorThrown) {
                console.error("Błąd zapisu:", textStatus);
            }

            $('#sproutvideo-url-input', element).change(function () {
                const url = $(this).val()
                if (initiallyValid(url)) {
                    updatePreviewUrl(url);
                }
            });

            $('.save-button', element).click(function () {
                const url = $('#sproutvideo-url-input', element).val();

                if (!initiallyValid(url)) {
                    runtime.notify('error', {
                        msg: 'Niepoprawny adres URL. Wprowadź pełny embed URL ze SproutVideo.'
                    });
                    return;
                }

                const handlerUrl = runtime.handlerUrl(element, 'save_video_url');

                $.ajax({
                    type: "POST",
                    url: handlerUrl,
                    data: JSON.stringify({video_url: url}),
                    success: saveSucceed,
                    error: saveFailed,
                });
            });
}

