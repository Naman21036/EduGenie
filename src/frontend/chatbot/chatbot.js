document.addEventListener(
    "DOMContentLoaded",
    () => {

        const messages =
        document.querySelectorAll(
            ".assistant-message"
        );

        messages.forEach(
            msg => {

                msg.style.opacity = 0;

                setTimeout(
                    () => {

                        msg.style.transition =
                        "0.5s";

                        msg.style.opacity = 1;

                    },
                    100
                );

            }
        );

    }
);